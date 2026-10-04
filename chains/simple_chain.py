from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableParallel


load_dotenv()

prompt = PromptTemplate(
    template = 'Generate 5 interesting facts about this {topic}',
    input_variables=['topic']
)

# Initialize the Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",  # Or "gemini-2.5-pro"
    temperature=0.7,
    max_completion_tokens=100
)

parser = StrOutputParser()

chain = prompt | model | parser

res = chain.invoke({'topic' : 'Cricket'})

print(res)

chain.get_graph().print_ascii()



