from fastapi import FastAPI

from app.api import documents
from app.api import embeddings
from app.api import indexing
from app.api import chat
app = FastAPI(
    title="AI Onboarding Assistant",
    description="Product documentation based AI assistant",
    version="1.0"
)


# Register API routes
app.include_router(
    documents.router
)
app.include_router(
    embeddings.router
)

app.include_router(
    indexing.router
)
app.include_router(
    chat.router
)

@app.get("/")
def home():
    return {
        "message": "AI Onboarding Assistant Running"
    }