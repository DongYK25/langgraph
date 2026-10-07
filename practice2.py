####多个输入

from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str

def process_values(state: AgentState) -> AgentState:
    """此函数处理多个不同的输入"""
    state['result'] = f"这里是{state['name']}!求和为{sum(state['values'])}"
    return state

def test1():
    graph = StateGraph(AgentState)
    graph.add_node("测试2",process_values)
    graph.set_entry_point("测试2")
    graph.set_finish_point("测试2")
    app = graph.compile()

    # from IPython.display import Image, display
    # display(Image(app.get_graph().draw_mermaid_png()))

    result = app.invoke({"name": "Bob","values":[1,2,3,4]})
    result["result"]
    print(result["result"])

import math

nums = [2,3,4]
res = math.prod(nums)

class AgentState2(TypedDict):
    values: List[int]
    name: str
    operation: str
    result: str

def process_values2(state: AgentState2) -> AgentState:
    """此函数处理多个不同的输入"""
    if state["operation"] == "*":
        res = math.prod(state['values'])
    elif state["operation"] == "+":
        res = sum(state['values'])
    state['result'] = f"你好{state['name']}!计算结果为{res}"
    return state

def test2():
    graph = StateGraph(AgentState2)
    graph.add_node("测试21",process_values2)
    graph.set_entry_point("测试21")
    graph.set_finish_point("测试21")
    app = graph.compile()

    # from IPython.display import Image, display
    # display(Image(app.get_graph().draw_mermaid_png()))

    result = app.invoke({"name": "Bob","values":[1,2,3,4],"operation":"+"})
    result["result"]
    print(result["result"])

test2()