import base64
import hashlib
import hmac
import os

_ITERATIONS = 260_000
_SALT_SIZE = 32


def hash_password(plain: str) -> str:
    salt = os.urandom(_SALT_SIZE)
    dk = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, _ITERATIONS)
    return base64.b64encode(salt + dk).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        raw = base64.b64decode(hashed.encode("utf-8"))
        salt, stored_dk = raw[:_SALT_SIZE], raw[_SALT_SIZE:]
        new_dk = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, _ITERATIONS)
        return hmac.compare_digest(stored_dk, new_dk)
    except Exception:
        return False
