from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional 
from app.schemas.schemas import PatientCreate, PatientOut, PatientUpdate
from app.models.models import Patient
from app.db.session import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.models.models import User
from app.core.dependencies import get_current_user
from app.crud import patient as crud_patient

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

@router.get("/", response_model=List[PatientOut])
def read_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_or_recepcionista)
):
    return crud_patient.get_patients(db, skip=skip, limit=limit)

@router.get("/{patient_id}", response_model=PatientOut)
def read_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_or_recepcionista)
):
    patient = crud_patient.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return patient

@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_or_recepcionista)
):
    db_patient = crud_patient.get_patient(db, patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return crud_patient.update_patient(db, db_patient, patient_update)

@router.delete("/{patient_id}", response_model=PatientOut)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_or_recepcionista)
):
    patient = crud_patient.delete_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return patient