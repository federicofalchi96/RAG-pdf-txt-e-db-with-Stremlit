from typing import Annotated, List, TypedDict, Optional, Literal
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.documents import Document

class GraphState(TypedDict):
    """
    Represents the State of our graph
    
    Attributes:

    """
    messages: Annotated[List[AnyMessage], add_messages]
    question: str
    documents: Optional[List[Document]]
    pdf_docs: List[Document]
    web_results: Optional[List]
    generated_response: Optional[str]
    needs_web: Optional[bool]