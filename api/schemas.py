from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class TicketCreate(BaseModel):
    description: str

class TicketResponse(BaseModel):
    ticket_id: str
    title: Optional[str]
    description: str
    category: Optional[str]
    subcategory: Optional[str]
    priority: Optional[str]
    status: str
    created_at: datetime
    resolution_steps: Optional[str]
    root_cause: Optional[str]

    class Config:
        from_attributes = True

class TraceResponse(BaseModel):
    ticket_id: str
    state: Dict[str, Any]
    next_nodes: List[str]
