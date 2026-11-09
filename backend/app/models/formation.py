# Permet d'obtenir automatiquement la date et l'heure actuelles
from datetime import datetime

# Importe l'objet db configuré dans extensions.py
from app.extensions import db


# Classe Python représentant la table "formations" dans MySQL
class Formation(db.Model):

    # Nom exact de la table dans la base de données
    __tablename__ = "formations"

    # Identifiant unique de chaque formation
    id = db.Column(db.Integer, primary_key=True)

    # Titre obligatoire de la formation
    titre = db.Column(db.String(150), nullable=False)

    # Description détaillée de la formation
    description = db.Column(db.Text, nullable=True)

    # Catégorie : informatique, gestion, marketing, etc.
    categorie = db.Column(db.String(100), nullable=True)

    # Durée : par exemple "3 mois" ou "40 heures"
    duree = db.Column(db.String(50), nullable=True)

    # Niveau : débutant, intermédiaire ou avancé
    niveau = db.Column(db.String(50), nullable=True)

    # État de la formation. Valeur par défaut : active
    statut = db.Column(db.String(30), default="active", nullable=False)

    # Date de création automatique de la formation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Date de modification automatique de la formation
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Transforme une formation en dictionnaire Python
    # Ce dictionnaire sera ensuite envoyé au frontend Angular en JSON
    def to_dict(self):
        return {
            "id": self.id,
            "titre": self.titre,
            "description": self.description,
            "categorie": self.categorie,
            "duree": self.duree,
            "niveau": self.niveau,
            "statut": self.statut,

            # Convertit la date en texte lisible par Angular
            "created_at": self.created_at.isoformat()
            if self.created_at else None,

            "updated_at": self.updated_at.isoformat()
            if self.updated_at else None,
        }
