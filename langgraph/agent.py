from langchain_ollama import ChatOllama
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START,END


llm = ChatOllama(model="gemma3:1b")


class AgentState(TypedDict):
    messages: List[HumanMessage]


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f" \nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START,"process")
graph.add_edge("process",END)

agent = graph.compile()

# png_bytes = agent.get_graph().draw_mermaid_png()
# with open("graph.png", "wb") as f:
#     f.write(png_bytes)
# print("saved graph.png")


user_input = input("Enter: ")

agent.invoke({'messages' : [HumanMessage(content=user_input)]})


