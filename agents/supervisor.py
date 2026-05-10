import json
from langchain_core.messages import SystemMessage, HumanMessage
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import TicketState
from config import get_llm
from agents.prompts import SUPERVISOR_PROMPT

def supervisor_node(state: TicketState):
    llm = get_llm()
    state_summary = {
        "category": state.get("category"),
        "diagnostics_present": bool(state.get("diagnostics")),
        "rag_present": bool(state.get("rag_results")),
        "resolution_present": bool(state.get("resolution_steps")),
        "confidence": state.get("confidence"),
        "requires_human_approval": state.get("requires_human_approval"),
        "status": state.get("status")
    }
    
    # Manual routing guardrails
    if not state.get("category"):
        return {"next": "triage"}
        
    if state.get("requires_human_approval") and state.get("status") != "approved":
        return {"next": "human_approval"}
        
    if state.get("status") in ["escalated", "resolved"]:
        return {"next": "end"}

    try:
        response = llm.invoke([
            SystemMessage(content=SUPERVISOR_PROMPT),
            HumanMessage(content=f"Current State Summary: {json.dumps(state_summary)}")
        ])
        content = response.content.strip()
        if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
        route = data.get("next", "end").lower()
        
        valid_routes = ["triage", "diagnose", "retrieve_knowledge", "resolve", "escalate", "human_approval", "end"]
        if route not in valid_routes:
            route = "end"
        return {"next": route}
    except Exception as e:
        print(f"Supervisor parsing error: {e}")
        return {"next": "escalate"}
