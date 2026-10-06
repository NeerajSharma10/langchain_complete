from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"chrome-extension://.*",
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load heavy models once at startup, not per request
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
llm = ChatHuggingFace(
    llm=HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        temperature=0.2,
    )
)
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

prompt = ChatPromptTemplate.from_template(
    """Answer the question using only the transcript context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}"""
)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

chain_cache = {}  # video_id -> rag_chain, so each video is embedded only once

def get_chain(video_id: str):
    if video_id in chain_cache:
        return chain_cache[video_id]

    transcript = YouTubeTranscriptApi().fetch(video_id)
    text = " ".join(item.text for item in transcript)
    chunks = splitter.create_documents([text])
    retriever = FAISS.from_documents(chunks, embeddings).as_retriever(
        search_kwargs={"k": 4}
    )
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )
    chain_cache[video_id] = chain
    return chain

class AskRequest(BaseModel):
    video_id: str
    question: str

@app.post("/ask")
def ask(req: AskRequest):
    try:
        return {"answer": get_chain(req.video_id).invoke(req.question)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))