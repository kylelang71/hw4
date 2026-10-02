import hashlib
import hmac
import secrets

_ALGORITHM = "pbkdf2_sha256"
_ITERATIONS = 120_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), _ITERATIONS)
    return f"{_ALGORITHM}${salt}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    algorithm, salt, digest_hex = stored_hash.split("$")
    if algorithm != _ALGORITHM:
        return False
    expected = bytes.fromhex(digest_hex)
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), _ITERATIONS)
    return hmac.compare_digest(actual, expected)
