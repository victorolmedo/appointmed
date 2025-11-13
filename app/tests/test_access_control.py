from app.models.models import UserRole
from app.tests.conftest import generate_token

def test_admin_can_access_patients(client):
    token = generate_token("admin@admin.com", UserRole.admin)
    response = client.get("/patients/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_professional_cannot_access_patients(client):
    token = generate_token("pro@med.com", UserRole.profesional)
    response = client.get("/patients/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
