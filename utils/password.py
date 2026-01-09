import base64
import hashlib
import hmac
import secrets


def hash_password(password: str, *, iterations: int = 210_000) -> str:
    if not password:
        raise ValueError("password is required")

    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    salt_b64 = base64.urlsafe_b64encode(salt).decode("ascii").rstrip("=")
    dk_b64 = base64.urlsafe_b64encode(dk).decode("ascii").rstrip("=")
    return f"pbkdf2_sha256${iterations}${salt_b64}${dk_b64}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        scheme, iters_s, salt_b64, dk_b64 = password_hash.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        iterations = int(iters_s)

        pad_salt = "=" * (-len(salt_b64) % 4)
        pad_dk = "=" * (-len(dk_b64) % 4)
        salt = base64.urlsafe_b64decode((salt_b64 + pad_salt).encode("ascii"))
        expected = base64.urlsafe_b64decode((dk_b64 + pad_dk).encode("ascii"))

        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False
