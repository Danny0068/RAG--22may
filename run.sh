#!/bin/bash

# Start the backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start the frontend
cd ../frontend
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 