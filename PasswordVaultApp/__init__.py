from flask import Flask,render_template,url_for,redirect,request
from flask_wtf import CSRFProtect
from .routes import register_routes
from PasswordVaultApp.extensions import db
from dotenv import load_dotenv
import os
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path="C:/Program Files/Python313/Flask_py/PasswordVault/encrypt.env")
def create_app():
  app=Flask(__name__)
  app.config['ENCRYPTION_KEY'] = os.getenv('ENCRYPTION_KEY')  # for Fernet
  print("ENCRYPTION_KEY from config:", app.config['ENCRYPTION_KEY'])
  app.config['SECRET_KEY']='d15da24a879a875aa6e68d379ec90888'
  #csrf.init_app(app)
  #Defining the location of the database
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))
  db_path = os.path.join(BASE_DIR, 'passwdcheck.db')
  app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False#To disable uneccessary event-tracking in SQL
  #need to bind the db object to the flask app context ass the db object was declared as global hence
  #we need to bind it with the app using this line
  db.init_app(app)
  register_routes(app)
  print("ENCRYPTION_KEY from config:", app.config['ENCRYPTION_KEY'])
  return app