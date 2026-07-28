from fastapi import APIRouter

from app.services.indexing_service import (
    index_documents
)


router = APIRouter()


@router.post("/index")
def create_index():

    return index_documents()