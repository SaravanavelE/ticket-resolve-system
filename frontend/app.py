import streamlit as st

st.set_page_config(
    page_title="Topaz OS | Intelligent Ticket Resolution",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Topaz OS Dashboard 🤖")
st.markdown("### Welcome to the Agentic AI-Powered IT Ticket Resolution System")

import os

# Basic Authentication for Public Demo
DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "")

if DEMO_PASSWORD:
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.warning("🔒 This demo is password protected.")
        pwd = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            if pwd == DEMO_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        st.stop()

st.markdown("""
Use the sidebar to navigate through the modules:
- **📥 Ticket Inbox**: View incoming tickets and their real-time statuses.
- **🔍 Processing Trace**: Inspect the exact agent reasoning and RAG sources used for a specific ticket.
- **📊 Analytics Dashboard**: View comprehensive system metrics.
""")


st.info("System is Online. Ready to process IT Tickets.")
