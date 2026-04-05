import bcrypt

# Hashing a password (e.g., at registration)
def hash_password(plain_password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=12)  # higher rounds = slower = more secure
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt)

# Verifying a password (e.g., at login)
def verify_password(plain_password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed)
