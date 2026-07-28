from fastapi import APIRouter
from app.services.embedding_service import (
    generate_embedding
)

from app.services.pinecone_service import (
    search_vectors
)

from app.services.llm_service import (
    generate_answer
)


router = APIRouter()


@router.get("/chat")
def chat(question):


    # 1. Convert question to vector

    query_embedding = generate_embedding(
        question
    )


    # 2. Search Pinecone

    results = search_vectors(
        query_embedding
    )


    # 3. Extract documents

    contexts = []

    for match in results.matches:

        contexts.append(
            match.metadata["text"]
        )


    context = "\n\n".join(contexts)


    # 4. Generate answer

    answer = generate_answer(
        context,
        question
    )


    return {
        "question": question,
        "answer": answer,
        "sources": contexts
    }