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


def index_documents():

    documents = load_documents(
        "documents/product_documentation.txt"
    )


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
            vector_id=f"chunk-{index}",

            embedding=vector,

            metadata={
                "text": texts[index],
                "source":
                "product_documentation.txt"
            }
        )


    return {
        "message":
        "Documents indexed successfully",

        "total_chunks":
        len(chunks)
    }