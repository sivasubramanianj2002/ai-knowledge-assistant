from fastapi import APIRouter

from app.services.document_service import (
    load_documents,
    split_documents
)


router = APIRouter()


@router.get("/documents")
def process_documents():

    documents = load_documents(
        "documents/product_documentation.txt"
    )

    chunks = split_documents(documents)

    return {
        "total_documents": len(documents),
        "total_chunks": len(chunks),
        "first_chunk": chunks[0].page_content
    }