from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.models import Patient
from typing import List, Optional
from app.schemas.schemas import PatientCreate, PatientUpdate
from app.core.security import hash_password


def create_patient(db: Session, patient: PatientCreate) -> Patient:
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
    return db.query(Patient).offset(skip).limit(limit).all()

def update_patient(db: Session, db_patient: Patient, patient_update: PatientUpdate) -> Patient:
    for field, value in patient_update.dict(exclude_unset=True).items():
        setattr(db_patient, field, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int) -> Optional[Patient]:
    patient = get_patient(db, patient_id)
    if patient:
        db.delete(patient)
        db.commit()
    return patient
