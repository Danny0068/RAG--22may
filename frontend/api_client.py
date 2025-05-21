import requests
import os
from typing import List, Dict, Any
from datetime import datetime

class APIClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv('BACKEND_URL', 'http://localhost:8000')
        if not self.base_url.endswith('/'):
            self.base_url += '/'

    def upload_documents(self, files: List[Any]) -> Dict:
        """Upload documents to the backend."""
        try:
            files_data = [
                ("files", (f.name, f, "application/pdf" if f.name.endswith(".pdf") else "image/jpeg"))
                for f in files
            ]
            response = requests.post(f"{self.base_url}upload/", files=files_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error uploading documents: {str(e)}")

    def list_documents(self) -> List[Dict]:
        """Get list of all uploaded documents."""
        try:
            response = requests.get(f"{self.base_url}documents/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching documents: {str(e)}")

    def query_documents(self, question: str, selected_docs: List[str] = None) -> Dict:
        """Query documents with a research question."""
        try:
            payload = {
                "question": question,
                "selected_docs": selected_docs or []
            }
            response = requests.post(f"{self.base_url}query/", json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error querying documents: {str(e)}") 