from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.vector_store import get_vector_store
from services.rag_engine import get_chat_engine

router = APIRouter()

# Define the expected JSON format from the frontend
class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_with_document(request: ChatRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    try:
        # 1. Connect to Pinecone
        vector_store = get_vector_store()
        
        # 2. Initialize the chat engine
        chat_engine = get_chat_engine(vector_store)
        
        # 3. Query the AI with the user's question
        response = chat_engine.chat(request.query)
        
        return {
            "answer": str(response),
            # Optional: Return the source nodes to show the user exactly where the AI got the info
            "sources": [node.text for node in response.source_nodes] 
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))