from app.core import security


# Monkey patch function we can use to shave a second off our tests by skipping the password hashing check
def verify_password_mock(first: str, second: str):
    return True


def test_login(client, test_user, monkeypatch):
    # Patch the test to skip password hashing check for speed
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    response = client.post(
        "/api/tokens",
        data={"username": test_user.email, "password": "nottheactualpass"},
    )
    assert response.status_code == 200


def test_wrong_password(client, test_db, test_user, test_password, monkeypatch):
    def verify_password_failed_mock(first: str, second: str):
        return False

    monkeypatch.setattr(security, "verify_password", verify_password_failed_mock)

    response = client.post(
        "/api/tokens", data={"username": test_user.email, "password": "wrong"}
    )
    assert response.status_code == 401


def test_wrong_login(client, test_db, test_user, test_password):
    response = client.post(
        "/api/tokens", data={"username": "fakeuser", "password": test_password}
    )
    assert response.status_code == 401
