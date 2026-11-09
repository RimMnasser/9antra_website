# Permet de demander le mot de passe sans l'afficher à l'écran
from getpass import getpass

# Importe l'application Flask
from app import create_app

# Importe la connexion à MySQL
from app.extensions import db

# Importe le modèle administrateur
from app.models.utilisateur import Utilisateur


# Crée l'application Flask
app = create_app()


# Utilise le contexte Flask pour accéder à MySQL
with app.app_context():
    # Demande l'email de l'administrateur
    email = input("Email administrateur : ").strip()

    # Demande le mot de passe sans l'afficher
    mot_de_passe = getpass("Mot de passe : ")

    # Vérifie si cet email existe déjà
    administrateur_existant = Utilisateur.query.filter_by(
        email=email
    ).first()

    if administrateur_existant:
        print("Cet administrateur existe déjà")
    else:
        # Crée le compte administrateur
        administrateur = Utilisateur(email=email, role="admin")

        # Transforme le mot de passe en hash sécurisé
        administrateur.definir_mot_de_passe(mot_de_passe)

        # Ajoute le compte dans la base de données
        db.session.add(administrateur)
        db.session.commit()

        print("Administrateur créé avec succès")
