import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.readers.file import PDFReader
from services.vector_store import get_vector_store

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
            
        # Explicitly map .pdf to the dedicated PDF reader
        extractor = {".pdf": PDFReader()}
        
        documents = SimpleDirectoryReader(
            input_files=[file_path], 
            file_extractor=extractor
        ).load_data()
        
        if not documents or not any(doc.text.strip() for doc in documents):
            raise HTTPException(status_code=400, detail="Document appears empty or unreadable.")
            
        vector_store = get_vector_store()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        VectorStoreIndex.from_documents(documents, storage_context=storage_context)
        
        return {"message": "Success", "chunks_created": len(documents)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)