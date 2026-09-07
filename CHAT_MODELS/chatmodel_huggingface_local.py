import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFacePipeline

# 1. Load configuration from .env file
load_dotenv()


# 2. Load the model directly using from_model_id
llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 100,
        "temperature": 0.1,
        "do_sample": True,
    },
)

# 3. Define prompt and run
prompt = "<|user|>\nwho is the mens singles number one ranked player in badminton?<|end|>\n<|assistant|>\n"

print("\nGenerating response...\n")
response = llm.invoke(prompt)

print(response)