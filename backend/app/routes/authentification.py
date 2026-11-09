# Blueprint crée un groupe de routes Flask
# request lit les données envoyées
# jsonify renvoie une réponse JSON
from flask import Blueprint, request, jsonify

# Crée un token JWT après une connexion réussie
from flask_jwt_extended import create_access_token

# Connexion à MySQL
from app.extensions import db

# Modèle de l'administrateur
from app.models.utilisateur import Utilisateur


# Groupe des routes d'authentification
# Les URLs commenceront par /api/auth
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


# POST /api/auth/connexion
# Permet à l'administrateur de se connecter
@auth_bp.post("/connexion")
def connecter_administrateur():
    # Récupère les données JSON envoyées par Angular
    donnees = request.get_json() or {}

    # Récupère l'email et le mot de passe envoyés
    email = donnees.get("email")
    mot_de_passe = donnees.get("mot_de_passe")

    # Vérifie que les deux champs sont présents
    if not email or not mot_de_passe:
        return jsonify({
            "erreur": "Email et mot de passe obligatoires"
        }), 400

    # Recherche l'administrateur avec son email
    utilisateur = Utilisateur.query.filter_by(email=email).first()

    # Vérifie l'existence du compte et le mot de passe
    if not utilisateur or not utilisateur.verifier_mot_de_passe(
        mot_de_passe
    ):
        return jsonify({
            "erreur": "Email ou mot de passe incorrect"
        }), 401

    # Crée un token JWT pour les futures requêtes protégées
    token = create_access_token(
        identity=str(utilisateur.id),
        additional_claims={"role": utilisateur.role}
    )

    # Retourne le token à Angular
    return jsonify({
        "message": "Connexion réussie",
        "access_token": token,
        "utilisateur": utilisateur.to_dict()
    }), 200
