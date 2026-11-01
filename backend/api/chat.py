import traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.vector_store import get_vector_store
from services.rag_engine import get_chat_engine

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_with_document(request: ChatRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    try:
        print(f"\n--- NEW CHAT REQUEST ---")
        print(f"1. Received query: '{request.query}'")
        
        vector_store = get_vector_store()
        print("2. Pinecone Vector Store connected.")
        
        engine = get_chat_engine(vector_store)
        print("3. Query Engine initialized successfully.")
        
        print("4. Sending query to OpenRouter...")
        response = engine.query(request.query)
        print("5. AI Response received!")
        
        return {
            "answer": str(response),
            "sources": [node.text for node in response.source_nodes] if hasattr(response, "source_nodes") else []
        }
        
    except Exception as e:
        print("\n❌ CRITICAL ERROR IN CHAT ENDPOINT:")
        traceback.print_exc()  # This forces the exact error to print in the terminal
        raise HTTPException(status_code=500, detail=f"Failed during chat: {str(e)}")