@echo off
call .\venv\Scripts\activate
streamlit run frontend/app.py --server.port 8501
