#THIS FILE IS STORING FUNCTIONS RELATED TO ENCRYPTION,PASSWORD STRENGTH CHECKING,KEY GENERATION
import os
import re
import hashlib
import secrets
import base64
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def _get_key() -> bytes:
    master = os.environ.get("ENCRYPTION_MASTER_KEY", "default-dev-key")
    return hashlib.sha256(master.encode()).digest()


def encrypt(plaintext: str) -> str:
    key = _get_key()
    iv = secrets.token_bytes(12)
    aesgcm = AESGCM(key)
    ct_with_tag = aesgcm.encrypt(iv, plaintext.encode("utf-8"), None)
    ct = ct_with_tag[:-16]
    tag = ct_with_tag[-16:]
    combined = iv + tag + ct
    return base64.b64encode(combined).decode("utf-8")


def decrypt(encoded: str) -> str:
    key = _get_key()
    data = base64.b64decode(encoded)
    iv = data[:12]
    tag = data[12:28]
    ct = data[28:]
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(iv, ct + tag, None)
    return plaintext.decode("utf-8")


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
    #converting the passwd to byte code and then to sha1 hashcode
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
