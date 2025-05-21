import os
import pytest
from app.services.supabase_service import SupabaseService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@pytest.mark.asyncio
async def test_supabase_connection():
    """Test basic Supabase connection and operations."""
    service = SupabaseService()
    
    # Test document storage
    test_content = b"Test document content"
    test_filename = "test.txt"
    test_metadata = {
        "type": "text/plain",
        "size": len(test_content)
    }
    
    # Store document
    doc_id = await service.store_document(
        file_content=test_content,
        filename=test_filename,
        metadata=test_metadata
    )
    assert doc_id is not None
    
    # List documents
    documents = await service.list_documents()
    assert len(documents) > 0
    assert any(doc["filename"] == test_filename for doc in documents)
    
    # Get document
    doc = await service.get_document(doc_id)
    assert doc is not None
    assert doc["filename"] == test_filename
    assert doc["metadata"] == test_metadata
    
    # Delete document
    success = await service.delete_document(doc_id)
    assert success is True
    
    # Verify deletion
    documents = await service.list_documents()
    assert not any(doc["filename"] == test_filename for doc in documents) 