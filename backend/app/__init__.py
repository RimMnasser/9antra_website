# Importe Flask pour créer l'application
from flask import Flask

# Importe la configuration du projet
from .config import Config

# Importe les extensions utilisées par Flask
from .extensions import db, migrate, jwt, CORS

# Importe les routes des formations
from app.routes.formations import formations_bp

# Importe les routes des documents
from app.routes.documents_cours import documents_bp

# Importe les routes d'authentification
from app.routes.authentification import auth_bp

# Importe les routes du chatbot
from app.routes.chatbot import chatbot_bp


# Fonction qui construit et configure l'application Flask
def create_app():
    # Crée l'application Flask
    app = Flask(__name__)

    # Charge les paramètres de configuration
    app.config.from_object(Config)

    # Connecte SQLAlchemy à Flask
    db.init_app(app)

    # Active les migrations de base de données
    migrate.init_app(app, db)

    # Active l'authentification JWT
    jwt.init_app(app)

    # Autorise Angular à communiquer avec Flask
    CORS(app)

    # Enregistre les routes des formations
    app.register_blueprint(formations_bp)

    # Enregistre les routes des documents
    app.register_blueprint(documents_bp)

    # Enregistre les routes d'authentification
    app.register_blueprint(auth_bp)

    # Enregistre les routes du chatbot
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")

    # Retourne l'application configurée
    return app