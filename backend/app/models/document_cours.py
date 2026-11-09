# Importe la date et l'heure actuelles
from datetime import datetime

# Importe la relation avec la base de données
from app.extensions import db


# Représente la table "documents_cours" dans MySQL
class DocumentCours(db.Model):
    # Définit le nom de la table
    __tablename__ = "documents_cours"

    # Identifiant unique du document
    id = db.Column(db.Integer, primary_key=True)

    # Nom affiché du fichier
    nom_fichier = db.Column(db.String(255), nullable=False)

    # Chemin où le fichier est enregistré sur le serveur
    chemin_fichier = db.Column(db.String(500), nullable=False)

    # Type du fichier : PDF, DOCX, PPTX, etc.
    type_fichier = db.Column(db.String(50), nullable=True)

    # Taille du fichier en octets
    taille = db.Column(db.Integer, nullable=True)

    # Formation à laquelle appartient le document
    formation_id = db.Column(
        db.Integer,
        db.ForeignKey("formations.id"),
        nullable=False
    )

    # Date d'importation du document
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relation Python entre DocumentCours et Formation
    formation = db.relationship(
        "Formation",
        backref=db.backref("documents", lazy=True)
    )

    # Transforme l'objet en dictionnaire pour l'envoyer à Angular
    def to_dict(self):
        return {
            "id": self.id,
            "nom_fichier": self.nom_fichier,
            "chemin_fichier": self.chemin_fichier,
            "type_fichier": self.type_fichier,
            "taille": self.taille,
            "formation_id": self.formation_id,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }
