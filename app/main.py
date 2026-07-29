import sys
from pathlib import Path

# Ensure project root is in Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, jsonify

from app.api import chat, documents, embeddings, indexing


app = Flask(__name__)

# Register API routes (Blueprints)
app.register_blueprint(documents.router)
app.register_blueprint(embeddings.router)
app.register_blueprint(indexing.router)
app.register_blueprint(chat.router)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Onboarding Assistant Running"
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)