from app.core.security import hash_password, verify_password


def test_hash_is_not_plaintext_and_is_bytes():
    hashed = hash_password("hunter2")
    assert isinstance(hashed, bytes)
    assert b"hunter2" not in hashed


def test_correct_password_verifies():
    assert verify_password("correct horse", hash_password("correct horse"))


def test_wrong_password_is_rejected():
    assert not verify_password("wrong", hash_password("correct horse"))


def test_same_password_gets_different_salts():
    assert hash_password("same") != hash_password("same")
