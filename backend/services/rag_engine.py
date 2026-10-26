from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.openrouter import OpenRouter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from core.config import settings

# 1. Configure the LLM (OpenRouter Free Auto-Router)
# 'openrouter/free' dynamically routes to the best available free model 
# (like NVIDIA Nemotron, Google Gemma, or Thinking Machines) at that exact second.
llm = OpenRouter(
    api_key=settings.OPENROUTER_API_KEY,
    model="openrouter/free", 
    max_tokens=1024,
)

# 2. Configure the Embedding Model (Runs locally, 100% free)
# BAAI/bge-small-en-v1.5 is extremely fast and requires a dimension of 384 in Pinecone
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# 3. Apply settings globally to LlamaIndex
Settings.llm = llm
Settings.embed_model = embed_model
Settings.chunk_size = 512
Settings.chunk_overlap = 50

def get_chat_engine(vector_store):
    """Creates a chat engine from the vector store index."""
    # Load the index directly from Pinecone
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    # Return a chat engine that remembers conversation history
    return index.as_chat_engine(chat_mode="condense_question", verbose=True)