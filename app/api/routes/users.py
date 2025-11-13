from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate, UserOut
from app.schemas.schemas import UserUpdate
from app.crud.user import create_user, get_user_by_email
from app.crud import user as crud_user
from app.core.dependencies import get_current_user

from app.db.session import SessionLocal
from app.core.dependencies import require_admin
from app.core.dependencies import require_roles
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/", response_model=UserOut)
# def create_user(user: UserCreate, db: Session = Depends(get_db), admin=Depends(require_roles("admin"))):
#     db_user = crud_user.get_user_by_email(db, user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email ya registrado")
#     return crud_user.create_user(db, user)

@router.post("/", response_model=UserOut)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)  # ✅ solo admins
):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return create_user(db, user)

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), admin=Depends(require_roles("admin"))):
    return crud_user.get_users(db, skip=skip, limit=limit)

@router.get("/me", response_model=UserOut)
def read_own_profile(user=Depends(get_current_user)):
    return user

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db), admin=Depends(require_roles("admin"))):
    db_user = crud_user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(require_roles("admin"))):
    user = crud_user.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_roles("admin"))
):
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    updated_user = crud_user.update_user(db, db_user, user_update)
    return updated_user


