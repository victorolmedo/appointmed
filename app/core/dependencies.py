from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import get_db
from app.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return {"email": user.email, "role": user.role, "id": user.id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def require_professional(user=Depends(get_current_user)):
    if user["role"] != "admin" and user["role"] != "professional":
        raise HTTPException(status_code=403, detail="Acceso restringido a profesionales")
    return user

# Nuevo: solo admin
def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acceso restringido a administradores")
    return user

# Nuevo: admin o recepcionista
def require_admin_or_recepcionista(user=Depends(get_current_user)):
    if user["role"] not in ["admin", "recepcionista"]:
        raise HTTPException(status_code=403, detail="Acceso restringido a recepcionistas o administradores")
    return user

def require_roles(*roles):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Acceso restringido")
        return user
    return checker
