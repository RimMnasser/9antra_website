# Importe la date et l'heure actuelles
from datetime import datetime

# Importe les fonctions de sécurité pour le mot de passe
from werkzeug.security import generate_password_hash, check_password_hash

# Importe la connexion à la base de données
from app.extensions import db


# Représente la table "utilisateurs" dans MySQL
class Utilisateur(db.Model):
    # Définit le nom de la table
    __tablename__ = "utilisateurs"

    # Identifiant unique de l'utilisateur
    id = db.Column(db.Integer, primary_key=True)

    # Adresse email utilisée pour la connexion
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Mot de passe stocké sous forme de hash sécurisé
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)

    # Rôle de l'utilisateur dans l'application
    role = db.Column(db.String(30), default="admin", nullable=False)

    # Date de création du compte
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Transforme un mot de passe en hash sécurisé
    def definir_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    # Vérifie un mot de passe lors de la connexion
    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(
            self.mot_de_passe_hash,
            mot_de_passe
        )

    # Prépare les données publiques à envoyer à Angular
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }
