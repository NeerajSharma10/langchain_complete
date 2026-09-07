import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Load environment variables from .env
load_dotenv()

# 2. Initialize Google Generative AI Embeddings with 32 dimensions
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    output_dimensionality=32  # Requests a 32-dimensional embedding vector
)

# 3. Define query
query = "who is the mens singles number one ranked player in badminton"

# 4. Generate query embedding
vector = embeddings.embed_query(query)

# 5. Output results
print(f"Query: '{query}'")
print(f"Vector Dimensions: {len(vector)}")
print("Embedding Vector:")
print(vector)