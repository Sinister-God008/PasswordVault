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
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-secret-key")

    app.config['ENCRYPTION_KEY'] = os.getenv("ENCRYPTION_KEY")
    if not app.config['ENCRYPTION_KEY']:
        raise RuntimeError("ENCRYPTION_KEY is not set")

    # -----------------------------
    # Database configuration
    # -----------------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, "passwdcheck.db")

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Railway sometimes provides postgres://, SQLAlchemy needs postgresql://
        database_url = database_url.replace("postgres://", "postgresql://")
    else:
        database_url = f"sqlite:///{db_path}"

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print("Database URL in use:", app.config['SQLALCHEMY_DATABASE_URI'])

    # -----------------------------
    # Initialize extensions
    # -----------------------------
    db.init_app(app)

    # -----------------------------
    # Register routes
    # -----------------------------
    register_routes(app)

    return app
