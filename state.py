from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class TicketState(TypedDict):
    ticket_id: str
    description: str
    title: Optional[str]
    messages: Annotated[List[BaseMessage], add_messages]
    category: Optional[str]
    subcategory: Optional[str]
    priority: Optional[str]
    entities: Optional[dict]
    diagnostics: Optional[List[str]]
    rag_results: Optional[List[dict]]
    resolution_steps: Optional[List[str]]
    confidence: Optional[float]
    status: str
    next: str
    requires_human_approval: bool
    escalation_reason: Optional[str]
