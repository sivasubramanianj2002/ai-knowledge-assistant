from pinecone import Pinecone

from app.core.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME
)


pc = Pinecone(
    api_key=PINECONE_API_KEY
)


index = pc.Index(
    PINECONE_INDEX_NAME
)


def insert_vector(
    vector_id,
    embedding,
    metadata
):

    index.upsert(
        vectors=[
            {
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            }
        ]
    )


def search_vectors(query_vector, top_k=3):

    result = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    return result
