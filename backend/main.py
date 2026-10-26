from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

# Import our new API routers
from api import upload, chat

settings.validate_keys()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend engine for the Document RAG System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the API endpoints
app.include_router(upload.router, prefix="/api", tags=["Documents"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME} is running.", "status": "online"}