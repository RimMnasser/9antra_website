from getpass import getpass
from app import create_app
from app.extensions import db
from app.models.utilisateur import Utilisateur

app = create_app()

with app.app_context():
    email = input("Email administrateur : ").strip()
    admin = Utilisateur.query.filter_by(email=email).first()

    if not admin:
        print("Administrateur introuvable")
    else:
        nouveau = getpass("Nouveau mot de passe : ")
        admin.definir_mot_de_passe(nouveau)
        db.session.commit()
        print("Mot de passe modifié avec succès")