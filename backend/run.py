from app import create_app
from app.extensions import db
from app.models.formation import Formation
# Importe le modèle pour que SQLAlchemy connaisse la table documents_cours
from app.models.document_cours import DocumentCours
# Importe le modèle pour permettre la création de la table
from app.models.utilisateur import Utilisateur

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables créées avec succès")


if __name__ == "__main__":
    app.run(debug=True)
