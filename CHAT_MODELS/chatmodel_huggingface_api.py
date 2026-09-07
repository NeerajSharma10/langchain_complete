from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3.8-27B",
    task="text-generation"
)

model = ChatHuggingFace(llm = llm)

response = model.invoke("Who is the prime minister of India")

print(response)


