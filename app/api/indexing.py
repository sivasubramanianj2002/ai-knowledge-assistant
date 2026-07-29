from pathlib import Path

from flask import Blueprint, jsonify, request

from app.services.indexing_service import index_documents

router = Blueprint("indexing", __name__)


@router.route("/index", methods=["POST"])
def create_index():
    source = request.args.get("source", default="product_documentation.txt")

    file_path = Path("documents") / source

    if not file_path.exists():
        return jsonify({
            "detail": f"File not found: {source}. Upload it first via POST /documents/upload"
        }), 404

    result = index_documents(str(file_path))
    return jsonify(result)

