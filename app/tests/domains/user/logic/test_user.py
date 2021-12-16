from app.domains.user.logic import get_password_hash, verify_password


def test_correct_password_verified():
    password = "123456qwert!@#$%фывап"

    hash_ = get_password_hash(password)
    assert verify_password(password, hash_)

    another_hash_ = get_password_hash(password)
    assert verify_password(password, another_hash_)


def test_incorrect_password_not_verified():
    password = "654321qwert!@#$%фывап"
    hash_ = get_password_hash(password)
    invalid_password = "654321QWERT!@#$%ФЫВАП"

    assert not verify_password(invalid_password, hash_)
