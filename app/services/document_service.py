from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCUMENTS_DIR = Path("documents")
ALLOWED_EXTENSIONS = {".txt", ".pdf"}


def load_documents(file_path: str):

    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(str(path))
    elif suffix == ".txt":
        loader = TextLoader(str(path))
    else:
        raise ValueError(
            f"Unsupported file type: {suffix}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    documents = loader.load()

    return documents


def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def save_upload(file_name: str, content: bytes) -> Path:

    suffix = Path(file_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {suffix}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = Path(file_name).name
    destination = DOCUMENTS_DIR / safe_name

    destination.write_bytes(content)

    return destination
