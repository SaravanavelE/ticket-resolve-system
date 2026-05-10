@echo off
echo =======================================================
echo  Topaz Agentic Ticket Resolution System Demo Launcher
echo =======================================================

call .\venv\Scripts\activate

echo.
echo [1/3] Starting FastAPI Backend on Port 8000...
start cmd /k "title FastAPI Backend && uvicorn api.main:app --reload --port 8000"

echo [2/3] Waiting for Backend to initialize...
timeout /t 5 >nul

echo [3/3] Starting Streamlit Frontend on Port 8501...
start cmd /k "title Streamlit Frontend && streamlit run frontend/app.py --server.port 8501"

echo.
echo Demo is running!
echo  - Frontend: http://localhost:8501
echo  - API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers.
pause
