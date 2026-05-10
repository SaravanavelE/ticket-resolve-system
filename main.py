from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database.models import get_db, init_db, Ticket

app = FastAPI(title="Topaz-Inspired Agentic AI-Powered Intelligent Ticket Resolution System")

@app.on_event("startup")
def on_startup():
    init_db()

class TicketResponse(BaseModel):
    ticket_id: str
    title: str
    category: str
    priority: str
    status: str

    class Config:
        from_attributes = True

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Ticket Resolution AI System is running."}

@app.get("/tickets", response_model=List[TicketResponse])
def get_tickets(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).offset(skip).limit(limit).all()
    return tickets

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.post("/classify")
def classify_ticket(ticket_text: str):
    # Stub for future LangGraph Agent classification
    # In full system, this would call the agent router
    return {
        "status": "processing",
        "message": "Ticket dispatched to Triage Agent",
        "predicted_agent": "Resolution Agent"
    }
