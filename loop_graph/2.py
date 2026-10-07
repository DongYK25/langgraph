from typing import TypedDict, List
import random
from langgraph.graph import StateGraph,START,END


class AgentState(TypedDict):
    name: str
    guess_input: int
    guess_output: List[int]
    counter: int
    lower_bound: int
    upper_bound: int
    complete_guess: bool


def greeting_node(state: AgentState) -> AgentState:
    """Greeting Node which says hi to the person"""
    state["name"] = f"Hi there, {state['name']},let's play a game"
    return state


def random_node(state: AgentState) -> AgentState:
    """Generates a random number for guess game"""
    guess1 = random.randint(state["lower_bound"], state["upper_bound"])
    # 从完整区间过滤掉aa里面的数字
    full_range = set(range(state["lower_bound"], state["upper_bound"] + 1))
    used = set(state["guess_output"])
    available = list(full_range - used)   # 剩下允许选的数字
    if state["guess_output"]:
        guess1 = random.choice(available)
    state["guess_output"].append(guess1)
    state["counter"] += 1
    if state["guess_input"] == guess1:
        state["complete_guess"]=True
    elif state["guess_input"] < guess1:
        state["upper_bound"] = guess1
    elif state["guess_input"] > guess1:
        state["lower_bound"] = guess1
    return state

def should_continue(state: AgentState) -> AgentState:
    """Function to decide what to do next"""
    if state["counter"] < 7 and state["complete_guess"] ==False:
        print("ENTERING LOOP", state["counter"],state["complete_guess"],state["lower_bound"],state["upper_bound"])
        return "loop"  # Continue looping
    else:
        return "exit"  # Exit the loop

graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random",  # Source node
    should_continue,  # Action
    {
        "loop": "random",  # Self‑loop back to same node
        "exit": END        # End the graph
    }
)
graph.set_entry_point("greeting")
# graph.add_edge(START, "greeting") 两者作用相同 
app = graph.compile()

initial_state = AgentState(name = "John",guess_input= 10,guess_output= [],lower_bound= 1,upper_bound=20,counter=0,complete_guess=False)
result = app.invoke(initial_state)
print(result)







