import sys, os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.graph import run_ticket_workflow, workflow_graph

def test_workflow():
    tickets = [
        {"id": "TKT-101", "desc": "User crystal forgot her active directory password and needs a reset. This is urgent."},
        {"id": "TKT-102", "desc": "Outlook keeps disconnecting from the Exchange server. Please help, my email is outbox stuck."},
        {"id": "TKT-103", "desc": "The server in Mumbai datacenter caught on fire and is physically destroyed."}
    ]
    
    for t in tickets:
        print(f"\n{'='*60}\nProcessing {t['id']}: {t['desc']}\n{'-'*60}")
        
        result = run_ticket_workflow(t["desc"], t["id"])
        
        if result:
            print("\n>>> Final State Snapshot <<<")
            print(f"Status: {result.get('status')}")
            print(f"Category: {result.get('category')} / Priority: {result.get('priority')}")
            print(f"Confidence: {result.get('confidence')}")
            print(f"Requires Approval: {result.get('requires_human_approval')}")
            
            if result.get("resolution_steps"):
                print("Resolution Steps:")
                for step in result.get("resolution_steps"):
                    print(f"  - {step}")
            if result.get("escalation_reason"):
                print(f"Escalated Because: {result.get('escalation_reason')}")
                
            # If requires human approval, simulate human approving
            if result.get("next") == "human_approval" or "human_approval" in str(workflow_graph.get_state({"configurable": {"thread_id": t["id"]}}).next):
                print("\n>>> INTERRUPT TRIGGERED: Human Approval Required <<<")
                print("Simulating human approval...")
                
                # Update state to approved
                config = {"configurable": {"thread_id": t["id"]}}
                workflow_graph.update_state(config, {"status": "approved"})
                
                # Resume graph by passing None
                result = workflow_graph.invoke(None, config)
                print("\n>>> Final State After Approval Snapshot <<<")
                print(f"Status: {result.get('status')}")
                print("Resolution Steps Updated:")
                for step in result.get("resolution_steps", []):
                    print(f"  - {step}")

if __name__ == "__main__":
    print("Graph Structure:\n")
    print(workflow_graph.get_graph().draw_mermaid())
    print("\nStarting Tests...")
    test_workflow()
