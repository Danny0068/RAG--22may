from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET
import json
from typing import List, Dict, Any, Optional
import uuid

class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.bucket = SUPABASE_BUCKET
        
        # Ensure bucket exists
        try:
            self.client.storage.get_bucket(self.bucket)
        except Exception:
            self.client.storage.create_bucket(self.bucket, {"public": True})  # Set to public for reading

    async def store_document(self, file_content: bytes, filename: str, metadata: Dict[str, Any]) -> str:
        """Store a document in Supabase storage and its metadata in the database."""
        try:
            # Validate file type and size
            if not self._validate_file(filename, len(file_content)):
                raise ValueError("Invalid file type or size")

            # Generate unique ID for the document
            doc_id = str(uuid.uuid4())
            
            # Store file in storage
            file_path = f"{doc_id}/{filename}"
            self.client.storage.from_(self.bucket).upload(
                file_path,
                file_content,
                {
                    "content-type": metadata.get("type", "application/octet-stream"),
                    "x-upsert": "true"  # Overwrite if exists
                }
            )
            
            # Store metadata in database
            self.client.table("documents").insert({
                "id": doc_id,
                "filename": filename,
                "file_path": file_path,
                "metadata": metadata
            }).execute()
            
            return doc_id
        except Exception as e:
            raise Exception(f"Error storing document: {str(e)}")

    def _validate_file(self, filename: str, size: int) -> bool:
        """Validate file type and size."""
        # Allowed file types
        allowed_types = {'.pdf', '.txt', '.doc', '.docx', '.jpg', '.jpeg', '.png'}
        
        # Check file extension
        if not any(filename.lower().endswith(ext) for ext in allowed_types):
            return False
            
        # Check file size (e.g., max 10MB)
        if size > 10 * 1024 * 1024:  # 10MB in bytes
            return False
            
        return True

    async def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document and its metadata from Supabase."""
        try:
            # Get metadata from database
            response = self.client.table("documents").select("*").eq("id", doc_id).execute()
            if not response.data:
                return None
                
            doc_data = response.data[0]
            
            # Get file content from storage
            file_content = self.client.storage.from_(self.bucket).download(doc_data["file_path"])
            
            return {
                "id": doc_id,
                "filename": doc_data["filename"],
                "content": file_content,
                "metadata": doc_data["metadata"]
            }
        except Exception as e:
            raise Exception(f"Error retrieving document: {str(e)}")

    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents with their metadata."""
        try:
            response = self.client.table("documents").select("*").execute()
            return [{
                "id": doc["id"],
                "filename": doc["filename"],
                "upload_date": doc["created_at"],
                "metadata": doc["metadata"]
            } for doc in response.data]
        except Exception as e:
            raise Exception(f"Error listing documents: {str(e)}")

    async def delete_document(self, doc_id: str) -> bool:
        """Delete a document and its metadata from Supabase."""
        try:
            # Get document metadata to find file path
            response = self.client.table("documents").select("file_path").eq("id", doc_id).execute()
            if not response.data:
                return False
                
            file_path = response.data[0]["file_path"]
            
            # Delete from storage
            self.client.storage.from_(self.bucket).remove([file_path])
            
            # Delete from database
            self.client.table("documents").delete().eq("id", doc_id).execute()
            
            return True
        except Exception as e:
            raise Exception(f"Error deleting document: {str(e)}") 