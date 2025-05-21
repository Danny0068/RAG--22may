---
title: RAG Document Research
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# RAG Document Research & Theme Identification

A Retrieval-Augmented Generation (RAG) system for document research and theme identification. This project uses FastAPI for the backend, Streamlit for the frontend, and Supabase for document storage.

## Features

- Document upload and processing (PDF, images)
- Theme identification and analysis
- Document citation tracking
- Interactive chat interface
- Persistent document storage with Supabase

## Quick Start with GitHub Codespaces

1. Click the "Code" button in this repository
2. Select the "Codespaces" tab
3. Click "Create codespace on main"
4. Once the codespace is ready, run:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
5. The application will be available at:
   - Frontend: https://[your-codespace-url]-8501.githubpreview.dev
   - Backend API: https://[your-codespace-url]-8000.githubpreview.dev

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   └── requirements.txt
└── docker-compose.yml
```

## Environment Variables

Create a `.env` file in the root directory:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GROQ_API_KEY=your_groq_api_key
```

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rag-document-research.git
cd rag-document-research
```

2. Install dependencies:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
pip install -r requirements.txt
```

3. Run the application:
```bash
# Using Docker Compose
docker-compose up

# Or run separately:
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
streamlit run app.py
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT License 