from sqlalchemy.orm import Session
from app.models.models import Appointment
from app.schemas.schemas import AppointmentCreate

def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
