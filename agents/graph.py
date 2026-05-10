from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import TicketState
from agents.supervisor import supervisor_node
from agents.nodes import triage_node, diagnose_node, retrieve_knowledge_node, resolve_node, escalate_node, human_approval_node
from langchain_core.messages import HumanMessage
from config import settings

def build_graph():
    builder = StateGraph(TicketState)
    
    # Add Nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("triage", triage_node)
    builder.add_node("diagnose", diagnose_node)
    builder.add_node("retrieve_knowledge", retrieve_knowledge_node)
    builder.add_node("resolve", resolve_node)
    builder.add_node("escalate", escalate_node)
    builder.add_node("human_approval", human_approval_node)
    
    # Add Edges
    builder.add_edge(START, "supervisor")
    
    builder.add_conditional_edges(
        "supervisor",
        lambda s: s["next"],
        {
            "triage": "triage",
            "diagnose": "diagnose",
            "retrieve_knowledge": "retrieve_knowledge",
            "resolve": "resolve",
            "escalate": "escalate",
            "human_approval": "human_approval",
            "end": END
        }
    )
    
    # All workers report back to supervisor
    for node in ["triage", "diagnose", "retrieve_knowledge", "resolve", "escalate", "human_approval"]:
        builder.add_edge(node, "supervisor")
        
    return builder

builder = build_graph()

# Setup Checkpointer (PostgresSaver for Production, MemorySaver for Dev/Local SQLite)
try:
    if "sqlite" not in settings.sync_database_url.lower():
        from langgraph.checkpoint.postgres import PostgresSaver
        import psycopg
        from psycopg.rows import dict_row
        
        # Setup PostgresSaver
        conn = psycopg.connect(settings.sync_database_url, row_factory=dict_row)
        memory = PostgresSaver(conn)
        memory.setup()
        print("LangGraph Checkpointer: PostgresSaver Connected")
    else:
        memory = MemorySaver()
        print("LangGraph Checkpointer: MemorySaver (SQLite fallback)")
except Exception as e:
    print(f"Failed to connect PostgresSaver, falling back to MemorySaver: {e}")
    memory = MemorySaver()

# Interrupt before the human_approval node to wait for user input
workflow_graph = builder.compile(checkpointer=memory, interrupt_before=["human_approval"])

def run_ticket_workflow(ticket_description: str, ticket_id: str):
    config = {"configurable": {"thread_id": ticket_id}}
    
    initial_state = {
        "ticket_id": ticket_id,
        "description": ticket_description,
        "messages": [HumanMessage(content=ticket_description)],
        "status": "open",
        "requires_human_approval": False
    }
    
    try:
        result = workflow_graph.invoke(initial_state, config)
        return result
    except Exception as e:
        print(f"Workflow failed: {e}")
        return None

if __name__ == "__main__":
    print(workflow_graph.get_graph().draw_mermaid())
