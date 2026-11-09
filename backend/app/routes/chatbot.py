from flask import Blueprint, request, jsonify
from app.services.chatbot_service import ChatbotService

chatbot_bp = Blueprint("chatbot", __name__)

# Chargement unique du service (évite de recharger le modèle à chaque requête)
_chatbot_service = None

def get_chatbot_service():
    global _chatbot_service
    if _chatbot_service is None:
        _chatbot_service = ChatbotService()
    return _chatbot_service


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint du chatbot
    Body JSON attendu : { "question": "ta question ici" }
    """
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({
            "success": False,
            "error": "Le champ 'question' est obligatoire"
        }), 400

    question = str(data["question"]).strip()

    if not question:
        return jsonify({
            "success": False,
            "error": "La question ne peut pas être vide"
        }), 400

    try:
        service = get_chatbot_service()
        reponse = service.repondre(question)

        return jsonify({
            "success": True,
            "reponse": reponse
        }), 200

    except Exception as e:
        print(f"Erreur chatbot : {e}")
        return jsonify({
            "success": False,
            "error": "Une erreur est survenue lors du traitement de la question"
        }), 500