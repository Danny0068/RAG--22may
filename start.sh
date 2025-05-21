#!/bin/bash

# Start the backend
cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start the frontend
cd /app/frontend
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 