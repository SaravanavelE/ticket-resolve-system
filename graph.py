from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
from state import TicketState
from config import get_llm
from agents.nodes import triage_node, diagnostic_node, knowledge_retrieval_node, resolution_node, escalation_node

def supervisor_node(state: TicketState):
    llm = get_llm()
    
    if not state.get("category"):
        return {"next": "triage"}
        
    system_prompt = """You are the Topaz Supervisor. Review the current state and decide the next step.
    Available routes: triage, diagnostic, knowledge_retrieval, resolution, escalation, end.
    Respond ONLY with the name of the next route. Nothing else.
    
    Rules:
    1. If category is missing -> triage
    2. If diagnostics are missing -> diagnostic
    3. If rag_results are missing -> knowledge_retrieval
    4. If resolution_steps are missing -> resolution
    5. If resolution needs approval or is done -> end
    6. If ticket is too complex -> escalation
    """
    
    state_str = f"Category: {state.get('category')}\nDiagnostics: {bool(state.get('diagnostics'))}\nRAG: {bool(state.get('rag_results'))}\nResolution: {bool(state.get('resolution_steps'))}"
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=state_str)])
    
    route = response.content.strip().lower()
    
    valid_routes = ["triage", "diagnostic", "knowledge_retrieval", "resolution", "escalation", "end"]
    if route not in valid_routes:
        route = "end"
        
    return {"next": route}

builder = StateGraph(TicketState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("triage", triage_node)
builder.add_node("diagnostic", diagnostic_node)
builder.add_node("knowledge_retrieval", knowledge_retrieval_node)
builder.add_node("resolution", resolution_node)
builder.add_node("escalation", escalation_node)

builder.add_edge(START, "supervisor")

builder.add_conditional_edges(
    "supervisor",
    lambda s: s["next"],
    {
        "triage": "triage",
        "diagnostic": "diagnostic",
        "knowledge_retrieval": "knowledge_retrieval",
        "resolution": "resolution",
        "escalation": "escalation",
        "end": END
    }
)

for node in ["triage", "diagnostic", "knowledge_retrieval", "resolution", "escalation"]:
    builder.add_edge(node, "supervisor")

memory = MemorySaver()
graph = builder.compile(
    checkpointer=memory,
    interrupt_before=["resolution"]  # Human-in-the-Loop
)

if __name__ == "__main__":
    # Test script block
    config = {"configurable": {"thread_id": "ticket_123"}}
    
    initial_state = {
        "ticket_id": "INC-45678",
        "description": "I cannot reset my password, my active directory account is locked.",
        "messages": [HumanMessage(content="User ticket: I cannot reset my password, my active directory account is locked.")],
        "status": "open"
    }
    
    print("Testing the graph execution...")
    try:
        # Note: If no real GROQ_API_KEY is in .env, this will error.
        result = graph.invoke(initial_state, config)
        print("Graph Final State:", result)
    except Exception as e:
        print(f"Graph run failed (likely missing API key): {e}")
