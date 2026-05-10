import streamlit as st
import requests
import json

import os

API_URL = os.environ.get("API_URL", "http://localhost:8000")


st.set_page_config(page_title="Processing Trace", page_icon="🔍", layout="wide")
st.title("🔍 Agent Processing Trace")

ticket_id = st.text_input("Enter Ticket ID (e.g. INC-XXX):")

if st.button("Fetch Trace") or ticket_id:
    if not ticket_id:
        st.warning("Please enter a Ticket ID")
    else:
        try:
            res = requests.get(f"{API_URL}/tickets/{ticket_id}/trace")
            if res.status_code == 200:
                data = res.json()
                state = data.get("state", {})
                next_nodes = data.get("next_nodes", [])
                
                st.header(f"Ticket: {ticket_id}")
                st.info(f"Current Status: **{state.get('status', 'Unknown').upper()}**")
                
                if "human_approval" in next_nodes:
                    st.warning("🚨 This ticket is awaiting Human Approval for a sensitive action.")
                    if st.button("Approve Action"):
                        app_res = requests.post(f"{API_URL}/tickets/{ticket_id}/approve")
                        if app_res.status_code == 200:
                            st.success("Approved successfully! Reloading...")
                            st.rerun()
                            
                with st.expander("📝 1. Triage Results", expanded=True):
                    st.write(f"**Category:** {state.get('category')}")
                    st.write(f"**Priority:** {state.get('priority')}")
                    st.write(f"**Entities Extract:** {state.get('entities')}")
                    st.write(f"**Confidence:** {state.get('confidence')}")

                with st.expander("🛠️ 2. Diagnostics Execution", expanded=True):
                    diags = state.get('diagnostics', [])
                    if diags:
                        for d in diags:
                            st.code(d)
                    else:
                        st.write("No diagnostics run.")

                with st.expander("📚 3. RAG Knowledge Retrieval", expanded=False):
                    rag = state.get('rag_results', [])
                    if rag:
                        for r in rag:
                            st.markdown(f"**Source:** `{r.get('metadata', {}).get('source')}`")
                            st.info(r.get('content'))
                    else:
                        st.write("No knowledge retrieved.")
                        
                with st.expander("✅ 4. Resolution Strategy", expanded=True):
                    steps = state.get('resolution_steps', [])
                    if steps:
                        for step in steps:
                            st.markdown(f"- {step}")
                    else:
                        st.write("No resolution steps generated.")
                        
                if state.get('escalation_reason'):
                    with st.expander("🚨 5. Escalation Details", expanded=True):
                        st.error(state.get('escalation_reason'))
                        
            else:
                st.error("Trace not found or ticket has not been processed by LangGraph yet.")
                if st.button("Process Ticket Now"):
                    res = requests.post(f"{API_URL}/tickets/{ticket_id}/process")
                    if res.status_code == 200:
                        st.success("Processed. Click Fetch Trace again.")
        except Exception as e:
            st.error(f"API Error: {e}")
