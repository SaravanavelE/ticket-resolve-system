#!/bin/bash
echo "======================================================="
echo " Topaz Agentic Ticket Resolution System Demo Launcher"
echo "======================================================="

source venv/bin/activate

echo -e "\n[1/3] Starting FastAPI Backend on Port 8000..."
uvicorn api.main:app --reload --port 8000 &
BACKEND_PID=$!

echo "[2/3] Waiting for Backend to initialize..."
sleep 5

echo "[3/3] Starting Streamlit Frontend on Port 8501..."
streamlit run frontend/app.py --server.port 8501 &
FRONTEND_PID=$!

echo -e "\nDemo is running!"
echo " - Frontend: http://localhost:8501"
echo " - API Docs: http://localhost:8000/docs"
echo -e "\nPress Ctrl+C to stop both servers."

trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT
wait
