from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate, UserOut
from app.crud.user import create_user, get_user_by_email
from app.db.session import SessionLocal
from app.core.dependencies import require_admin
from app.core.dependencies import require_roles

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return create_user(db, user)

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