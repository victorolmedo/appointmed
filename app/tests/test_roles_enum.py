from app.models.models import UserRole

def test_user_roles_enum():
    expected_roles = {"admin", "recepcionista", "profesional"}
    actual_roles = {role.value for role in UserRole}
    assert actual_roles == expected_roles, f"Roles definidos: {actual_roles}"
