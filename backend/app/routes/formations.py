from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
# Vérifie qu'un token JWT valide est présent
from flask_jwt_extended import jwt_required


from app.models.formation import Formation

formations_bp = Blueprint("formations", __name__, url_prefix="/api/formations")


@formations_bp.get("")
@jwt_required()
def lister_formations():
    formations = Formation.query.all()
    return jsonify([formation.to_dict() for formation in formations])


@formations_bp.post("")
@jwt_required()
def creer_formation():
    donnees = request.get_json()

    if not donnees or not donnees.get("titre"):
        return jsonify({"erreur": "Le titre est obligatoire"}), 400

    formation = Formation(
        titre=donnees["titre"],
        description=donnees.get("description"),
        categorie=donnees.get("categorie"),
        duree=donnees.get("duree"),
        niveau=donnees.get("niveau"),
        statut=donnees.get("statut", "active")
    )

    db.session.add(formation)
    db.session.commit()

    return jsonify(formation.to_dict()), 201


@formations_bp.put("/<int:formation_id>")
@jwt_required()
def modifier_formation(formation_id):
    # Recherche la formation par son identifiant
    # Retourne automatiquement une erreur 404 si elle n'existe pas
    formation = Formation.query.get_or_404(formation_id)

    # Récupère les nouvelles données envoyées
    donnees = request.get_json() or {}

    # Modifie uniquement les champs reçus
    formation.titre = donnees.get("titre", formation.titre)
    formation.description = donnees.get(
        "description", formation.description
    )
    formation.categorie = donnees.get(
        "categorie", formation.categorie
    )
    formation.duree = donnees.get("duree", formation.duree)
    formation.niveau = donnees.get("niveau", formation.niveau)
    formation.statut = donnees.get("statut", formation.statut)

    # Enregistre les modifications dans MySQL
    db.session.commit()

    # Retourne la formation modifiée
    return jsonify(formation.to_dict()), 200


@formations_bp.delete("/<int:formation_id>")
@jwt_required()
def supprimer_formation(formation_id):
    # Recherche la formation à supprimer
    formation = Formation.query.get_or_404(formation_id)

    # Supprime la formation de la session SQLAlchemy
    db.session.delete(formation)

    # Valide définitivement la suppression dans MySQL
    db.session.commit()

    # Retourne un message de confirmation
    return jsonify({
        "message": "Formation supprimée avec succès"
    }), 200
   

# GET /api/formations
# Récupère toutes les formations


    # GET /api/formations/<formation_id>
    # Récupère une formation précise avec son identifiant
@formations_bp.get("/<int:formation_id>")
@jwt_required()
def obtenir_formation(formation_id):
    # Recherche la formation dans la base MySQL
    # Retourne automatiquement une erreur 404 si elle n'existe pas
    formation = Formation.query.get_or_404(formation_id)

    # Transforme la formation en JSON et retourne un succès HTTP 200
    return jsonify(formation.to_dict()), 200




