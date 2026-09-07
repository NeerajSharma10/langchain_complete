import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Load environment variables
load_dotenv()

model_name = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

print(f"Loading local embedding model '{model_name}' via Hugging Face...")

# 2. Initialize the local HuggingFace Embeddings wrapper
# "cpu" will be used by default, or "cuda" if you have a GPU set up.
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

# 3. Define multiple questions (Badminton, Cricket, Hockey)
questions = [
    # Badminton
    "who is the mens singles number one ranked player in badminton",
    "What is the standard net height in a badminton match?",
    # Cricket
    "Who won the most ICC Cricket World Cup titles?",
    "How many runs are awarded when a batsman hits the ball over the boundary line without bouncing?",
    # Hockey
    "Which country won the maximum Olympic gold medals in men's field hockey?",
    "How many periods are played in a standard ice hockey game?"
]

# 4. Generate embeddings for all questions locally
print("Generating list of embeddings locally...\n")
vectors = embeddings.embed_documents(questions)

# 5. Output inspection
print(f"Total Sentences Processed: {len(vectors)}")
print(f"Vector Dimensionality: {len(vectors[0])}\n")

for i, (q, vec) in enumerate(zip(questions, vectors), start=1):
    print(f"[{i}] Question: '{q}'")
    print(f"    Vector preview (first 5 dimensions): {vec[:5]}")
    print("-" * 65)