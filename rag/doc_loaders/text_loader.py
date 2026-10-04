from langchain_community.document_loaders import TextLoader
import os

file_path = os.path.join(os.path.dirname(__file__), "rag.txt")
loader = TextLoader(file_path,  encoding="utf-8")

docs = loader.load()

print(docs[0].page_content)
