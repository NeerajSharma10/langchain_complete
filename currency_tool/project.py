from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import requests
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace



llm = ChatHuggingFace(
    llm=HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        temperature=0.2,
    )
)

@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """
    This function fetches a base currency conversion factor to target currency
    """
    url = f'https://v6.exchangerate-api.com/v6/0003a804f3dfb0140fe08702/pair/{base_currency}/{target_currency}'

    response = requests.get(url)
    return response.json()


# data = get_conversion_factor.invoke({
#     'base_currency' : 'usd',
#     'target_currency': 'inr'
# })

# if data["result"] == "success":
#     rate = data["conversion_rate"]
#     print(rate)


@tool
def convert(base_currency_value: int, conversion_rate: float) -> float:
    """
    Given a currency conversion rate, this function calculates the target currecny from given base value 
    """
    return base_currency_value*conversion_rate

# tool binding
llm_with_tools = llm.bind_tools([get_conversion_factor, convert])


