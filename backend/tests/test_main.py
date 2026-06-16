from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine

# Automatically create tables in the test database (e.g. SQLite)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_login_invalid():
    response = client.post(
        "/auth/login",
        json={"email": "nonexistent@user.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
