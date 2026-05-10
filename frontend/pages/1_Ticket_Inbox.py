import streamlit as st
import requests
import pandas as pd

import os

API_URL = os.environ.get("API_URL", "http://localhost:8000")


st.set_page_config(page_title="Ticket Inbox", page_icon="📥", layout="wide")
st.title("📥 Ticket Inbox")

col1, col2 = st.columns([1, 4])
status_filter = col1.selectbox("Filter by Status", ["All", "Open", "pending_approval", "resolved", "escalated", "Closed"])

with st.spinner("Loading tickets..."):
    url = f"{API_URL}/tickets/"
    if status_filter != "All":
        url += f"?status={status_filter}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            tickets = res.json()
            if not tickets:
                st.info("No tickets found.")
            else:
                df = pd.DataFrame(tickets)
                display_cols = ["ticket_id", "title", "category", "priority", "status", "created_at"]
                
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                
                def color_status(val):
                    color = 'green' if val == 'resolved' else 'orange' if val == 'pending_approval' else 'red' if val in ['escalated', 'Error'] else 'white'
                    return f'color: {color}'
                
                st.dataframe(df[display_cols].style.applymap(color_status, subset=['status']), use_container_width=True)
                
        else:
            st.error("Failed to fetch tickets")
    except Exception as e:
        st.error(f"Cannot connect to API: {e}")

st.markdown("---")
st.subheader("Simulate New Ticket")
desc = st.text_area("Ticket Description")
if st.button("Submit New Ticket"):
    try:
        res = requests.post(f"{API_URL}/tickets/", json={"description": desc})
        if res.status_code == 200:
            st.success(f"Ticket Created: {res.json()['ticket_id']}. Processing in background...")
    except Exception as e:
        st.error(f"Error: {e}")
