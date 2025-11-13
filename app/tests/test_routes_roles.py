import inspect
from fastapi import Depends
from app.api.routes import users, appointments, patients

def extract_dependencies(router):
    deps = []
    for route in router.router.routes:
        if hasattr(route, "endpoint"):
            sig = inspect.signature(route.endpoint)
            for param in sig.parameters.values():
                if isinstance(param.default, Depends):
                    deps.append(param.default.dependency)
    return deps

def test_users_routes_require_roles():
    deps = extract_dependencies(users)
    assert any("require_roles" in str(dep) for dep in deps), "Faltan roles en users.py"

def test_appointments_routes_require_roles():
    deps = extract_dependencies(appointments)
    assert any("require_roles" in str(dep) or "require_admin_or_recepcionista" in str(dep) for dep in deps), "Faltan roles en appointments.py"

def test_patients_routes_require_roles():
    deps = extract_dependencies(patients)
    assert any("require_roles" in str(dep) or "require_admin_or_recepcionista" in str(dep) for dep in deps), "Faltan roles en patients.py"
