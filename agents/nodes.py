import json
from langchain_core.messages import HumanMessage, SystemMessage
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import TicketState
from config import get_llm
from agents.tools import fetch_user_details, fetch_logs, reset_password, check_service_status, restart_service
from agents.prompts import TRIAGE_PROMPT, DIAGNOSE_PROMPT, RESOLVE_PROMPT, ESCALATE_PROMPT
from rag.retriever import TicketRAG

def triage_node(state: TicketState):
    llm = get_llm()
    prompt = f"{TRIAGE_PROMPT}\nTicket Description: {state.get('description')}"
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
        
        return {
            "category": data.get("category", "Unknown"),
            "subcategory": data.get("subcategory", "Unknown"),
            "priority": data.get("priority", "Medium"),
            "entities": data.get("entities", {}),
            "confidence": float(data.get("confidence", 0.5)),
            "status": "in_progress"
        }
    except Exception as e:
        return {"category": "Error", "confidence": 0.0, "status": "escalated"}

def diagnose_node(state: TicketState):
    llm = get_llm()
    tools = [fetch_user_details, fetch_logs, check_service_status]
    tool_llm = llm.bind_tools(tools)
    
    ctx = f"Desc: {state.get('description')}\nCat: {state.get('category')}\nEntities: {state.get('entities')}"
    response = tool_llm.invoke([
        SystemMessage(content=DIAGNOSE_PROMPT),
        HumanMessage(content=ctx)
    ])
    
    diagnostics = state.get("diagnostics", []) or []
    if hasattr(response, 'tool_calls') and response.tool_calls:
        diagnostics.append(f"Tools executed: {response.tool_calls}")
    else:
        diagnostics.append(response.content)

    return {"diagnostics": diagnostics}

def retrieve_knowledge_node(state: TicketState):
    rag = TicketRAG()
    query = f"{state.get('description', '')} {state.get('category', '')}"
    results = rag.retrieve_for_ticket(query)
    return {"rag_results": results}

def resolve_node(state: TicketState):
    llm = get_llm()
    ctx = f"Desc: {state.get('description')}\nDiag: {state.get('diagnostics')}\nRAG: {state.get('rag_results')}"
    try:
        response = llm.invoke([
            SystemMessage(content=RESOLVE_PROMPT),
            HumanMessage(content=ctx)
        ])
        content = response.content.strip()
        if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
        
        req_approval = bool(data.get("requires_human_approval", False))
        return {
            "resolution_steps": data.get("resolution_steps", [str(data)]),
            "confidence": float(data.get("confidence", 0.5)),
            "requires_human_approval": req_approval,
            "status": "pending_approval" if req_approval else "resolved"
        }
    except Exception as e:
        return {"resolution_steps": ["Error generating resolution"], "confidence": 0.0, "status": "escalated"}

def escalate_node(state: TicketState):
    llm = get_llm()
    ctx = f"Ticket: {state.get('description')}\nDiagnostics: {state.get('diagnostics')}"
    try:
        response = llm.invoke([
            SystemMessage(content=ESCALATE_PROMPT),
            HumanMessage(content=ctx)
        ])
        content = response.content.strip()
        if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
        
        return {
            "escalation_reason": data.get("escalation_reason", "Complex issue requiring human support"),
            "status": "escalated"
        }
    except Exception as e:
        return {"escalation_reason": "Escalated automatically due to failure.", "status": "escalated"}

def human_approval_node(state: TicketState):
    if state.get("status") == "approved":
        return {"requires_human_approval": False, "status": "resolved", "resolution_steps": state.get("resolution_steps", []) + ["Human approved the action."]}
    return {"status": "escalated", "escalation_reason": "Human rejected the proposed resolution."}
