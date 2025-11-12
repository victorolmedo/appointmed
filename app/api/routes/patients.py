from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import PatientCreate, PatientOut
from app.models.models import Patient
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.core.dependencies import require_admin_or_recepcionista

@router.post("/", response_model=PatientOut)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin_or_recepcionista)  # ✅ solo recepcionistas o admins
):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient
