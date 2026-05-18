from passlib.context import CryptContext

_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return _context.hash(plain)


def verify_password(plain: str, password_hash: str) -> bool:
    return _context.verify(plain, password_hash)
