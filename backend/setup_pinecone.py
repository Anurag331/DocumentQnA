from pinecone import Pinecone, ServerlessSpec
from core.config import settings

# Initialize Pinecone using the key from your .env file
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

print("Creating index... this takes about 30 seconds.")
pc.create_index(
    name="doc-qa",
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
print("✅ Success! Your vector index is ready.")