from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import GEMINI_API_KEY


embeddings = GoogleGenerativeAIEmbeddings(
     model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY
)


def generate_embedding(text: str):
    """
    Generate embedding for a single text chunk.
    """

    return embeddings.embed_query(text)