# Permet de créer une route Flask et de retourner du JSON
# send_file permet d’envoyer un fichier au navigateur
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required

# Permet de sécuriser le nom du fichier
from werkzeug.utils import secure_filename

# Permet de gérer les chemins et les dossiers
import os
# Protège les routes documents avec JWT
from flask_jwt_extended import jwt_required

# Connexion à MySQL
from app.extensions import db

# Modèles utilisés par cette route
from app.models.formation import Formation
from app.models.document_cours import DocumentCours


# Groupe de routes pour les documents de cours
# URL finale : /api/formations/<id>/documents
documents_bp = Blueprint(
    "documents",
    __name__,
    url_prefix="/api/formations"
)


# Extensions de fichiers autorisées
EXTENSIONS_AUTORISEES = {"pdf", "doc", "docx", "ppt", "pptx"}


# Vérifie si le fichier possède une extension autorisée
def extension_autorisee(nom_fichier):
    return (
        "." in nom_fichier
        and nom_fichier.rsplit(".", 1)[1].lower()
        in EXTENSIONS_AUTORISEES
    )


# POST /api/formations/<formation_id>/documents
# Importe un fichier et l'associe à une formation
@documents_bp.post("/<int:formation_id>/documents")
@auth_required()
def importer_document(formation_id):
    # Vérifie que la formation existe dans MySQL
    formation = Formation.query.get_or_404(formation_id)

    # Récupère le fichier envoyé dans le champ "fichier"
    fichier = request.files.get("fichier")

    # Vérifie qu'un fichier a bien été envoyé
    if not fichier or fichier.filename == "":
        return jsonify({
            "erreur": "Aucun fichier envoyé"
        }), 400

    # Vérifie l'extension du fichier
    if not extension_autorisee(fichier.filename):
        return jsonify({
            "erreur": "Type de fichier non autorisé"
        }), 400

    # Nettoie le nom du fichier pour éviter les noms dangereux
    nom_fichier = secure_filename(fichier.filename)

    # Construit le chemin vers le dossier backend/uploads
    dossier_uploads = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
    )

    # Crée le dossier s'il n'existe pas
    os.makedirs(dossier_uploads, exist_ok=True)

    # Chemin final du fichier sur le serveur
    chemin_complet = os.path.join(dossier_uploads, nom_fichier)

    # Enregistre physiquement le fichier dans uploads
    fichier.save(chemin_complet)

    # Récupère l'extension du fichier
    type_fichier = nom_fichier.rsplit(".", 1)[1].lower()

    # Crée l'enregistrement associé à la formation
    document = DocumentCours(
        nom_fichier=nom_fichier,
        chemin_fichier=chemin_complet,
        type_fichier=type_fichier,
        taille=os.path.getsize(chemin_complet),
        formation_id=formation.id
    )

    # Ajoute le document à la base de données
    db.session.add(document)
    db.session.commit()

    # Retourne les informations du document créé
    return jsonify(document.to_dict()), 201
# GET /api/formations/<formation_id>/documents
# Retourne tous les documents associés à une formation
@documents_bp.get("/<int:formation_id>/documents")
@jwt_required()
def lister_documents(formation_id):
    # Vérifie que la formation existe
    Formation.query.get_or_404(formation_id)

    # Recherche les documents liés à cette formation
    documents = DocumentCours.query.filter_by(
        formation_id=formation_id
    ).all()

    # Convertit chaque document en dictionnaire JSON
    resultat = [document.to_dict() for document in documents]

    # Retourne la liste des documents avec le statut 200
    return jsonify(resultat), 200

# GET /api/formations/documents/<document_id>/download
# Télécharge un document précis
@documents_bp.get("/documents/<int:document_id>/download")
@jwt_required()
def telecharger_document(document_id):
    # Recherche le document dans MySQL
    document = DocumentCours.query.get_or_404(document_id)

    # Envoie le fichier au navigateur
    # as_attachment=True force le téléchargement
    # download_name conserve le nom original
    return send_file(
        document.chemin_fichier,
        as_attachment=True,
        download_name=document.nom_fichier
    )


# DELETE /api/formations/documents/<document_id>
# Supprime le fichier et ses informations dans MySQL
@documents_bp.delete("/documents/<int:document_id>")
@jwt_required()
def supprimer_document(document_id):
    # Recherche le document dans MySQL
    document = DocumentCours.query.get_or_404(document_id)

    # Vérifie que le fichier existe physiquement sur le serveur
    if os.path.exists(document.chemin_fichier):
        # Supprime le fichier du dossier backend/uploads
        os.remove(document.chemin_fichier)

    # Supprime les informations du document dans MySQL
    db.session.delete(document)

    # Valide définitivement la suppression
    db.session.commit()

    # Retourne un message de confirmation
    return jsonify({
        "message": "Document supprimé avec succès"
    }), 200
