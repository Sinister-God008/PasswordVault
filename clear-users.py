from PasswordVaultApp import create_app
from PasswordVaultApp.extensions import db
from PasswordVaultApp.models import User

app = create_app()

with app.app_context():
    deleted = User.query.delete()
    db.session.commit()
    print(f"✅ Deleted {deleted} users.")
