import hashlib
import secrets
import hmac

from database.db import create_user, get_user_by_email


def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        310000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_hash):
    try:
        salt, original_hash = stored_hash.split("$")

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            310000
        ).hex()

        return hmac.compare_digest(new_hash, original_hash)

    except (ValueError, AttributeError):
        return False


def register_user(full_name, email, password):
    password_hash = hash_password(password)

    return create_user(
        full_name.strip(),
        email.strip().lower(),
        password_hash
    )


def authenticate_user(email, password):
    user = get_user_by_email(email.strip().lower())

    if user and verify_password(password, user[3]):
        return {
            "id": user[0],
            "full_name": user[1],
            "email": user[2],
            "role": user[4]
        }

    return None