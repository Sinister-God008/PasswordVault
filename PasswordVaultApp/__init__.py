from flask import Flask
from dotenv import load_dotenv
from pathlib import Path
import os

from PasswordVaultApp.extensions import db
from .routes import register_routes

def create_app():
    app = Flask(__name__)

    # -----------------------------
    # Load local .env ONLY for development
    # -----------------------------
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    # -----------------------------
    # App Configuration
    # -----------------------------

    # Flask secret key (sessions, CSRF)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-secret-key")

    # Encryption key for Fernet
    app.config['ENCRYPTION_KEY'] = os.getenv("ENCRYPTION_KEY")
    if not app.config['ENCRYPTION_KEY']:
        raise RuntimeError("ENCRYPTION_KEY is not set")

    # Database configuration
    # Priority: DATABASE_URL env variable (cloud DB), fallback to local SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, "passwdcheck.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.getenv("DATABASE_URL") or f"sqlite:///{db_path}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # -----------------------------
    # Initialize extensions
    # -----------------------------
    db.init_app(app)

    # -----------------------------
    # Register routes
    # -----------------------------
    register_routes(app)

    return app
