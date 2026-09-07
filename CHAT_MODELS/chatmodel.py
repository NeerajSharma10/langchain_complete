import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",  # Or "gemini-2.5-pro"
    temperature=0.7,
    max_completion_tokens=10
)

# Invoke the model directly
response = llm.invoke("Suggest me 5 indian male names.")

print(response.content[0]["text"])