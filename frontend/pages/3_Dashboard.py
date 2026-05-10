import streamlit as st
import requests
import pandas as pd
import plotly.express as px

import os

API_URL = os.environ.get("API_URL", "http://localhost:8000")


st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 System Analytics Dashboard")

try:
    res = requests.get(f"{API_URL}/dashboard/stats")
    if res.status_code == 200:
        stats = res.json()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tickets", stats["total"])
        col2.metric("Resolved", stats["resolved"])
        col3.metric("Escalated", stats["escalated"])
        col4.metric("Resolution Rate", f"{stats['resolution_rate']}%")
        
        st.markdown("---")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Tickets by Category")
            cats = stats["categories"]
            if cats:
                df_cats = pd.DataFrame(list(cats.items()), columns=["Category", "Count"])
                fig = px.pie(df_cats, values='Count', names='Category', hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No categorical data yet.")
                
        with col_chart2:
            st.subheader("Resolution vs Escalation")
            df_status = pd.DataFrame([
                {"Status": "Resolved", "Count": stats["resolved"]},
                {"Status": "Escalated", "Count": stats["escalated"]}
            ])
            fig2 = px.bar(df_status, x="Status", y="Count", color="Status")
            st.plotly_chart(fig2, use_container_width=True)
            
    else:
        st.error("Failed to load dashboard statistics.")
except Exception as e:
    st.error(f"Cannot connect to API: {e}")
