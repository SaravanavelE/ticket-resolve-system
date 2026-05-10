from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import uuid

from api.schemas import TicketCreate, TicketResponse, TraceResponse
from api.dependencies import get_db
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.models import Ticket
from agents.graph import workflow_graph, run_ticket_workflow

router = APIRouter()

@router.post("/tickets/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    ticket_id = f"INC{str(uuid.uuid4().int)[:8]}"
    new_ticket = Ticket(
        ticket_id=ticket_id,
        description=ticket.description,
        title="Pending Classification",
        status="Open"
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    
    # Run processing in background
    background_tasks.add_task(process_ticket_task, ticket_id, ticket.description, db)
    return new_ticket

def process_ticket_task(ticket_id: str, description: str, db: Session):
    result = run_ticket_workflow(description, ticket_id)
    if result:
        # Re-fetch in background
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        if ticket:
            ticket.category = result.get("category")
            ticket.priority = result.get("priority")
            ticket.status = result.get("status", "In Progress")
            if result.get("resolution_steps"):
                ticket.resolution_steps = "\\n".join(result.get("resolution_steps"))
            db.commit()

@router.get("/tickets/", response_model=List[TicketResponse])
def list_tickets(skip: int = 0, limit: int = 50, status: str = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if status:
        query = query.filter(Ticket.status == status)
    return query.order_by(Ticket.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.post("/tickets/{ticket_id}/process")
def process_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    result = run_ticket_workflow(ticket.description, ticket.ticket_id)
    if result:
        ticket.category = result.get("category")
        ticket.priority = result.get("priority")
        ticket.status = result.get("status", "In Progress")
        if result.get("resolution_steps"):
            ticket.resolution_steps = "\\n".join(result.get("resolution_steps"))
        db.commit()
    return {"message": "Processing complete", "state": result}

@router.get("/tickets/{ticket_id}/trace")
def get_trace(ticket_id: str):
    config = {"configurable": {"thread_id": ticket_id}}
    try:
        state_snapshot = workflow_graph.get_state(config)
        if not state_snapshot or not state_snapshot.values:
            raise HTTPException(status_code=404, detail="No trace found. Has it been processed?")
        
        values = state_snapshot.values
        # Remove un-serializable objects
        safe_values = {k: v for k, v in values.items() if k != "messages"}
        return {"ticket_id": ticket_id, "state": safe_values, "next_nodes": state_snapshot.next}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tickets/{ticket_id}/approve")
def approve_ticket(ticket_id: str, db: Session = Depends(get_db)):
    config = {"configurable": {"thread_id": ticket_id}}
    state_snapshot = workflow_graph.get_state(config)
    if not state_snapshot.next or "human_approval" not in state_snapshot.next:
        raise HTTPException(status_code=400, detail="Ticket is not awaiting approval.")
    
    workflow_graph.update_state(config, {"status": "approved"})
    result = workflow_graph.invoke(None, config)
    
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket and result:
        ticket.status = result.get("status")
        if result.get("resolution_steps"):
            ticket.resolution_steps = "\\n".join(result.get("resolution_steps"))
        db.commit()
        
    return {"message": "Approved and resumed.", "state": result}

@router.get("/dashboard/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Ticket).count()
    resolved = db.query(Ticket).filter(Ticket.status == "resolved").count()
    escalated = db.query(Ticket).filter(Ticket.status == "escalated").count()
    
    categories = db.query(Ticket.category, func.count(Ticket.id)).group_by(Ticket.category).all()
    cat_dist = {cat if cat else "Uncategorized": count for cat, count in categories}
    
    return {
        "total": total,
        "resolved": resolved,
        "escalated": escalated,
        "resolution_rate": round((resolved / total) * 100, 2) if total > 0 else 0,
        "categories": cat_dist
    }
