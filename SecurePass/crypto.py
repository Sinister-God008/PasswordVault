#THIS FILE IS STORING FUNCTIONS RELATED TO ENCRYPTION,PASSWORD STRENGTH CHECKING,KEY GENERATION
import os
import re
import hashlib
import requests
from cryptography.fernet import Fernet

#helps generate the encryption_master_key
print(Fernet.generate_key().decode())

#getting the environment master key from the environment variables/.env file
def _get_key() -> bytes:
    master = os.environ.get("ENCRYPTION_MASTER_KEY")
    if master is None:
        raise RuntimeError("ENCRYPTION_MASTER_KEY must be set")
    return master.encode()

#encrypts the password and secrets of user using fernet object and cryptography lib
def encrypt(plaintext: str) -> str:
    #creating a fernet object for the generated key
    f = Fernet(_get_key())
    return f.encrypt(plaintext.encode()).decode()

#decrypts the passwords and secrets of the user using fernet object and cryptography lib
def decrypt(token: str) -> str:
    f = Fernet(_get_key())
    return f.decrypt(token.encode()).decode()


def password_strength(password: str) -> int:
    if not password:
        return 0
    score = 0
    if len(password) >= 8:
        score += 10
    if len(password) >= 12:
        score += 15
    if len(password) >= 16:
        score += 15
    if len(password) >= 20:
        score += 10
    if re.search(r"[a-z]", password):
        score += 10
    if re.search(r"[A-Z]", password):
        score += 10
    if re.search(r"[0-9]", password):
        score += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        score += 20
    #creating a list where data is checking what all parameters are satisfied and then taking its sum
    variety = sum([
        bool(re.search(r"[a-z]", password)),
        bool(re.search(r"[A-Z]", password)),
        bool(re.search(r"[0-9]", password)),
        bool(re.search(r"[^a-zA-Z0-9]", password)),
    ])
    if variety >= 3: score += 5
    if variety == 4: score += 5
    #checks for weak patterns like only aplhas,numbers,repeating chars
    if re.match(r"^[a-zA-Z]+$", password):
        score -= 10
    if re.match(r"^[0-9]+$", password):
        score -= 15
    if re.search(r"(.)\1{2,}", password):
        score -= 10
    return max(0, min(100, score))


def strength_label(score: int) -> str:
    if score >= 80: return "Strong"
    if score >= 60: return "Good"
    if score >= 40: return "Fair"
    return "Weak"


def check_hibp_password(password: str) -> int:
    #converting the passwd to byte code and then to sha1 hashcode as HIBP uses it
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    #splitting the hashcode to prefix and suffix
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        #sending only the prefix to HIBP api to get matching results
        resp = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={"Add-Padding": "true"},
            timeout=5,
        )
        if not resp.ok:
            return 0
        #checking if returned result from HIBP match the suffix as well to verify breached data
        for line in resp.text.splitlines():
            parts = line.split(":")
            if len(parts) == 2 and parts[0].strip() == suffix:
                return int(parts[1].strip())
    except Exception:
        pass
    return 0
