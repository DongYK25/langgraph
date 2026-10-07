from typing import TypedDict, Dict
from langgraph.graph import StateGraph,START,END


class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    finalNumber: int


def adder(state: AgentState) -> AgentState:
    """This node adds the 2 numbers"""
    state["finalNumber"] = state["number1"] + state["number2"]
    return state

def subtractor(state: AgentState) -> AgentState:
    """This node subtracts the 2 numbers"""
    state["finalNumber"] = state["number1"] - state["number2"]
    return state


def decide_next_node(state: AgentState) -> AgentState:
    """This node will select the next node of the graph"""
    if state["operation"] == "+":
        return "addition_operation"
    elif state["operation"] == "-":
        return "subtraction_operation"

def decide_next_node2(state: AgentState) -> AgentState:
    """This node will select the next node of the second graph"""
    if state["operation"] == "+":
        return "addition_operation2"
    elif state["operation"] == "-":
        return "subtraction_operation2"

def test1():
    graph = StateGraph(AgentState)
    graph.add_node("add_node", adder)
    graph.add_node("subtract_node", subtractor)
    graph.add_node("router", lambda state:state)

    graph.add_edge(START, "router")

    graph.add_conditional_edges(
        "router",
        decide_next_node,
        {
            # Edge: Node
            "addition_operation": "add_node",
            "subtraction_operation": "subtract_node"
        }
    )

    graph.add_edge("add_node", END)
    graph.add_edge("subtract_node", END)

    app = graph.compile()



    # from IPython.display import Image, display
    # display(Image(app.get_graph().draw_mermaid_png()))

    result = app.invoke({"number1": 40,"number2":20,"operation":"-"})
    print(result)
    test1 = AgentState(number1=40,number2=10,operation="-")
    result2 = app.invoke(test1)
    print(result2)

def test2():
    class AgentState2(TypedDict):
        number1: int 
        operation: str
        number2: int
        finalNumber: int
        number3: int
        operation2: str
        number4: int
        finalNumber2: int

    graph = StateGraph(AgentState2)
    graph.add_node("add_node", adder)
    graph.add_node("subtract_node", subtractor)
    graph.add_node("router", lambda state:state)
    graph.add_node("add_node2", adder)
    graph.add_node("subtract_node2", subtractor)
    graph.add_node("router2", lambda state:state)

    graph.add_edge(START, "router")

    graph.add_conditional_edges(
        "router",
        decide_next_node,
        {
            # Edge: Node
            "addition_operation": "add_node",
            "subtraction_operation": "subtract_node"
        }
    )

    graph.add_edge("add_node", "router2")
    graph.add_edge("subtract_node", "router2")

    graph.add_conditional_edges(
        "router2",
        decide_next_node2,
        {
            # Edge: Node
            "addition_operation2": "add_node2",
            "subtraction_operation2": "subtract_node2"
        }
    )

    graph.add_edge("add_node2", END)
    graph.add_edge("subtract_node2", END)

    app = graph.compile()



    # from IPython.display import Image, display
    # display(Image(app.get_graph().draw_mermaid_png()))


    initial_state = AgentState2(number1 = 10, operation="-", number2 = 5, number3 = 7, number4=2, operation2="+", finalNumber= 0, finalNumber2 = 0)
    result2 = app.invoke(initial_state)
    print(result2)

test2()