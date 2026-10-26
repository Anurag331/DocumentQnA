from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from core.config import settings

def get_vector_store(index_name: str = "doc-qa"):
    """Initializes and returns the Pinecone vector store."""
    # 1. Initialize Pinecone client
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    
    # 2. Connect to your specific index
    # (Make sure you named your index 'doc-qa' in the Pinecone dashboard, 
    # or change this string to match what you named it)
    pinecone_index = pc.Index(index_name)
    
    # 3. Wrap it in LlamaIndex's VectorStore abstraction
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    
    return vector_store