from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.api.routes import appointments
from app.api.routes import patients
from app.api.routes import users
from app.api.routes import auth


from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, SecurityScheme
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi


app = FastAPI(title="Sistema de Gestión de Citas")
app.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configurar CORS para permitir acceso desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sistema de Gestión de Citas",
        version="0.1.0",
        description="API para gestión de citas médicas",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi