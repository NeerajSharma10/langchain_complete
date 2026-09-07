import os
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize the Gemini model
llm = GoogleGenerativeAI(
    model="gemini-3.6-flash",  # Or "gemini-2.5-pro"
    temperature=0.7,
)

# Invoke the model directly
response = llm.invoke("Explain dark matter in two simple sentences.")

print(response)