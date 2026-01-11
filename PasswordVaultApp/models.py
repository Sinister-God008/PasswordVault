from PasswordVaultApp.extensions import db
from datetime import datetime

# --------------------------
# 1. User Model
# --------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True ,nullable=False)
    email = db.Column(db.String(120), unique=True ,nullable=False)
    password = db.Column(db.String(40), nullable=False)  # Store hashed password
    # Relationship to folders
    folders = db.relationship('Folder', backref='owner', lazy=True)


# --------------------------
# 2. Folder Model
# --------------------------
class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship to PasswordEntries
    passwords = db.relationship('PasswordEntry', backref='folder', lazy=True, cascade='all, delete')


# --------------------------
# 3. PasswordEntry Model
# --------------------------
class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # hashed password
    url = db.Column(db.String(255), nullable=True)

    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=False)
