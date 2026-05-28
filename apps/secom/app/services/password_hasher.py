import hashlib
import secrets

_ALGORITHM = "sha256"
_ITERATIONS = 100_000
_SALT_BYTES = 16


def hash_password(plain: str) -> str:
    salt = secrets.token_hex(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        _ALGORITHM,
        plain.encode("utf-8"),
        salt.encode("utf-8"),
        _ITERATIONS,
    ).hex()
    return f"pbkdf2_sha256${_ITERATIONS}${salt}${digest}"


def verify_password(plain: str, hashed: str) -> bool:
    try:
        scheme, iterations_s, salt, expected = hashed.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            _ALGORITHM,
            plain.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations_s),
        ).hex()
        return secrets.compare_digest(digest, expected)
    except (ValueError, TypeError):
        return False

