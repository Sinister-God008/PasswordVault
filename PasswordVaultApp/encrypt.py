from cryptography.fernet import Fernet
from flask import current_app

def encrypt_password(plaintext):
    key = current_app.config['ENCRYPTION_KEY'].encode()
    fernet = Fernet(key)
    return fernet.encrypt(plaintext.encode()).decode()

def decrypt_password(ciphertext):
    key = current_app.config['ENCRYPTION_KEY'].encode()
    fernet = Fernet(key)
    return fernet.decrypt(ciphertext.encode()).decode()
