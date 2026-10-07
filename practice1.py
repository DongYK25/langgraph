from typing import TypedDict, Dict
from langgraph.graph import StateGraph


class MessagesState(TypedDict):
    messages: str


# We now create an AgentState - shared data structure that keeps track of information as your application runs.
class AgentState(TypedDict):
    message : str


def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to the state"""
    state['message'] = "Hey " + state["message"] + ", how is your day going?"
    return state


graph = StateGraph(AgentState)

graph.add_node("greeter", greeting_node)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()


# from IPython.display import Image, display
# display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"message": "Bob"})

result["message"]


print(result["message"])