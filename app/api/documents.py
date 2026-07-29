from pathlib import Path

from flask import Blueprint, jsonify, request

from app.services.document_service import (
    load_documents,
    save_upload,
    split_documents,
    ALLOWED_EXTENSIONS,
)

router = Blueprint("documents", __name__)


@router.route("/documents", methods=["GET"])
def process_documents():
    source = request.args.get("source", default="product_documentation.txt")

    file_path = Path("documents") / source

    if not file_path.exists():
        return jsonify({
            "detail": f"File not found: {source}"
        }), 404

    documents = load_documents(str(file_path))

    chunks = split_documents(documents)

    return jsonify({
        "source": source,
        "total_documents": len(documents),
        "total_chunks": len(chunks),
        "first_chunk": chunks[0].page_content if chunks else ""
    })


@router.route("/documents/upload", methods=["POST"])
def upload_document():
    if "file" not in request.files:
        return jsonify({"detail": "No file uploaded in request"}), 400

    file = request.files["file"]

    if not file or file.filename == "":
        return jsonify({"detail": "No file selected for upload"}), 400

    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        return jsonify({
            "detail": f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        }), 400

    content = file.read()
    if not content:
        return jsonify({"detail": "Uploaded file is empty"}), 400

    saved_path = save_upload(file.filename, content)

    documents = load_documents(str(saved_path))
    chunks = split_documents(documents)

    return jsonify({
        "message": "File uploaded successfully",
        "filename": saved_path.name,
        "path": str(saved_path),
        "total_pages": len(documents),
        "total_chunks": len(chunks),
        "first_chunk": chunks[0].page_content if chunks else ""
    })

