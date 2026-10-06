import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough





from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

llm_endpoint = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",   # or "Qwen/Qwen2.5-7B-Instruct"
    task="text-generation",
    max_new_tokens=512,
    temperature=0.2,
)
llm = ChatHuggingFace(llm=llm_endpoint)


video_id = "4Vz6L8B73i4"

# 1. Fetch Transcript
try:
    # 1. Instantiate the API class
    yt_api = YouTubeTranscriptApi()

    # 2. Call .fetch() on the instance
    transcript_list = yt_api.fetch(video_id)

    # 3. Access text using attribute notation (.text) or dictionary key ['text']
    full_text = " ".join([item.text for item in transcript_list])

except Exception as e:
    print(f"Error fetching transcript: {e}")


splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
    chunk_overlap=200)

chunks = splitter.create_documents([full_text])

# print(len(chunks))

# print(chunks[0])

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},                 # use "cuda" if you have a GPU
    encode_kwargs={"normalize_embeddings": True},   # better similarity scores
)

vector_store = FAISS.from_documents(chunks, embeddings)

# first_id = vector_store.index_to_docstore_id[0]
# first_doc = vector_store.docstore.search(first_id)
# print(first_doc.page_content)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
# docs = retriever.invoke("What is the video about?")
# print(docs)




def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

prompt = ChatPromptTemplate.from_template(
    """Answer the question using only the transcript context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}"""
)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke("What is the video about?"))