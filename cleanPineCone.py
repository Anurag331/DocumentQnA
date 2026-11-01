import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("doc-qa")

# Delete all vectors in the index
index.delete(delete_all=True)
print("✅ Successfully cleared all corrupted vectors from doc-qa!")