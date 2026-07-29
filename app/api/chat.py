from flask import Blueprint, jsonify, request

from app.services.chat_service import chat as run_chat

router = Blueprint("chat", __name__)


@router.route("/chat", methods=["GET"])
def chat():
    question = request.args.get("question")

    if not question:
        return jsonify({
            "detail": "Missing required query parameter: 'question'"
        }), 400

    res = run_chat(question)

    return jsonify(res)