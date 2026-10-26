import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from llama_index.core import Document, VectorStoreIndex, StorageContext
from services.vector_store import get_vector_store
import pypdf

router = APIRouter()
TEMP_DIR = "temp_docs"

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        
    file_path = os.path.join(TEMP_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Robust PDF text extraction using pypdf directly
        extracted_text = ""
        if file.filename.endswith(".pdf"):
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        else:
            # Fallback for plain text files
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                extracted_text = f.read()
                
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract readable text from this file.")
            
        # Wrap the clean text into a LlamaIndex Document
        documents = [Document(text=extracted_text)]
        
        # Connect to Pinecone and store vectors
        vector_store = get_vector_store()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        VectorStoreIndex.from_documents(
            documents, 
            storage_context=storage_context
        )
        
        return {
            "message": f"Successfully processed and embedded '{file.filename}'", 
            "chunks_created": len(documents)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)