from pathlib import Path

from app.services.document_service import (
    load_documents,
    split_documents
)

from app.services.embedding_service import (
    embeddings
)

from app.services.pinecone_service import (
    insert_vector
)


def index_documents(
    file_path: str = "documents/product_documentation.txt"
):

    path = Path(file_path)
    source_name = path.name

    documents = load_documents(str(path))

    chunks = split_documents(
        documents
    )

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    vectors = embeddings.embed_documents(
        texts
    )

    for index, vector in enumerate(vectors):

        insert_vector(
            vector_id=f"{source_name}-chunk-{index}",

            embedding=vector,

            metadata={
                "text": texts[index],
                "source": source_name
            }
        )

    return {
        "message": "Documents indexed successfully",
        "source": source_name,
        "total_chunks": len(chunks)
    }
