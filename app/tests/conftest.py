import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.models import UserRole
from app.core.security import create_access_token

@pytest.fixture
def client():
    return TestClient(app)

def generate_token(email: str, role: UserRole, user_id: int = 1):
    payload = {
        "sub": email,
        "role": role.value,
        "id": user_id
    }
    return create_access_token(payload)
