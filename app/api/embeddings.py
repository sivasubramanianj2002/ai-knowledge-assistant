from flask import Blueprint, jsonify

from app.services.embedding_service import generate_embedding

router = Blueprint("embeddings", __name__)


@router.route("/embedding", methods=["GET"])
def test_embedding():

    vector = generate_embedding(
        "JWT authentication is used."
    )

    return jsonify({
        "dimension": len(vector),
        "first_10_values": vector[:10]
    })