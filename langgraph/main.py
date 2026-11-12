from typing import Dict, TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display

class AgentState(TypedDict):
    message : str

def greeting_node(state : AgentState) -> AgentState:
    """Simple node thats adds a greeting message to state"""

    state['message'] = 'Hey' + state['message'] + ' How is your day'
    return state

graph = StateGraph(AgentState)

graph.add_node('greeter', greeting_node)
graph.set_entry_point('greeter')
graph.set_finish_point('greeter')

app = graph.compile()

png_bytes = app.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_bytes)
print("saved graph.png")


result = app.invoke({'message' : 'Neeraj'})

print(result['message'])

