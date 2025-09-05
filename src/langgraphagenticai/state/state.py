from typing_extensions import TypedDict
from langgraph.graph.message import add_messages, Messages
from typing import Annotated , List

class State(TypedDict):
    """
    Represents the structure of the state used in the graph
    """
    messages: Annotated[List, add_messages]