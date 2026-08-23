from app.auth.security import create_access_token, decode_access_token, hash_password, verify_password


def test_hash_and_verify_password():
    hashed = hash_password("alumno123")
    assert hashed != "alumno123"
    assert verify_password("alumno123", hashed) is True
    assert verify_password("incorrecta", hashed) is False


def test_create_and_decode_access_token():
    token = create_access_token(subject="22040251")
    assert decode_access_token(token) == "22040251"


def test_decode_invalid_token_returns_none():
    assert decode_access_token("no-es-un-token-real") is None
