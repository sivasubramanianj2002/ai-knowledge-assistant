from fastapi import APIRouter

from app.services.embedding_service import generate_embedding

router = APIRouter()


@router.get("/embedding")
def test_embedding():

    vector = generate_embedding(
        "JWT authentication is used."
    )

    return {
        "dimension": len(vector),
        "first_10_values": vector[:10]
    }