from PasswordVaultApp import create_app
from PasswordVaultApp.extensions import db
from PasswordVaultApp.models import User, Folder, PasswordEntry

app = create_app()

with app.app_context():
    print("\n🔐 Checking database contents...\n")

    users = User.query.all()
    folders = Folder.query.all()
    passwords = PasswordEntry.query.all()

    if users:
        print("👤 Users:")
        for user in users:
            print(f"- ID: {user.id}, Username: {user.username}, Email: {user.email}")
    else:
        print("❌ No users found.\n")

    print("\n📂 Folders:")
    if folders:
        for folder in folders:
            print(f"- ID: {folder.id}, Name: {folder.name}, User ID: {folder.user_id}")
    else:
        print("❌ No folders found.\n")

    print("\n🔑 Passwords:")
    if passwords:
        for pwd in passwords:
            print(f"- ID: {pwd.id}, Title: {pwd.title}, Folder ID: {pwd.folder_id}")
    else:
        print("❌ No passwords found.\n")
