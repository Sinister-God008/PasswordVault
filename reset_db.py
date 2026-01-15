import os
from PasswordVaultApp import create_app
from PasswordVaultApp.extensions import db

# Match this path to the one used in __init__.py
db_path = os.path.join(os.path.dirname(__file__), 'PasswordVaultApp', 'passwdcheck.db')

if os.path.exists(db_path):
    os.remove(db_path)
    print("✅ Old database deleted.")
else:
    print("ℹ️ No existing database file found.")

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ New database created successfully.")
