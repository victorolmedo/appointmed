from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from sqlalchemy import cast, Date
from app.schemas.schemas import AppointmentCreate, AppointmentOut
from app.crud.appointment import create_appointment
from app.db.session import SessionLocal
from app.core.dependencies import require_roles
from app.core.dependencies import require_professional
from app.core.dependencies import require_admin_or_recepcionista
from app.core.dependencies import get_current_user 
from app.schemas.schemas import AppointmentFilter,WeeklyAgendaFilter
from typing import List
from app.models.models import Appointment
from fastapi.responses import StreamingResponse
import csv
import io

router = APIRouter()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AppointmentOut)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    #user=Depends(require_admin_or_recepcionista)
    user=Depends(require_roles("admin", "recepcionista"))
):
    # Validación 1: superposición de horario
    existing = db.query(Appointment).filter(
        Appointment.professional_id == appointment.professional_id,
        Appointment.date == appointment.date,
        Appointment.time == appointment.time
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="El profesional ya tiene una cita en ese horario")

    # Validación 2: duplicado por paciente
    duplicate = db.query(Appointment).filter(
        Appointment.patient_id == appointment.patient_id,
        func.date(Appointment.date) == appointment.date.date()
    ).first()

    if duplicate:
        raise HTTPException(status_code=400, detail="El paciente ya tiene una cita ese día")

    # Crear cita
    new_appointment = Appointment(
        date=appointment.date,
        time=appointment.time,
        service_type=appointment.service_type,
        status=appointment.status or "pendiente",
        patient_id=appointment.patient_id,
        professional_id=appointment.professional_id
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


@router.post("/agenda", response_model=List[AppointmentOut])
def get_agenda(
    agenda_filter: AppointmentFilter,
    db: Session = Depends(get_db),
    user=Depends(require_roles("recepcionista", "admin", "profesional"))
):
    professional_id = (
        agenda_filter.professional_id if user["role"] != "profesional" else user["id"]
    )

    query = db.query(Appointment).filter(
        Appointment.professional_id == professional_id if professional_id else Appointment.professional_id != None, # filtrar por profesional
        func.date(Appointment.date) == agenda_filter.date,
        Appointment.status == agenda_filter.status
    )
    #print("Consulta SQL:", str(query.statement.compile(compile_kwargs={"literal_binds": True})))
    return query.order_by(Appointment.date.asc(), Appointment.time.asc()).all()



@router.post("/agenda/semana", response_model=List[AppointmentOut])
def get_weekly_agenda(
    agenda_filter: WeeklyAgendaFilter,
    db: Session = Depends(get_db),
    user=Depends(require_roles("recepcionista", "admin", "profesional"))
):
    professional_id = (
        agenda_filter.professional_id if user["role"] != "profesional" else user["id"]
    )

    query = db.query(Appointment).filter(
        Appointment.professional_id == professional_id,
        cast(Appointment.date, Date) >= agenda_filter.start_date,
        cast(Appointment.date, Date) <= agenda_filter.end_date
    )

    if agenda_filter.status:
        query = query.filter(Appointment.status == agenda_filter.status)
        
   # print("Consulta SQL:", str(query.statement.compile(compile_kwargs={"literal_binds": True})))
    return query.order_by(Appointment.date.asc(), Appointment.time.asc()).all()




@router.get("/agenda/all", response_model=List[AppointmentOut])
def get_all_appointments(
    limit: int = 100,
    offset: int = 0,
    export_csv: bool = False,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    query = db.query(Appointment).filter(Appointment.date != None)
    query = query.order_by(Appointment.date.asc(), Appointment.time.asc())
    appointments = query.offset(offset).limit(limit).all()

    if export_csv:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "date", "time", "service_type", "status", "patient_id", "professional_id"])
        for a in appointments:
            writer.writerow([
                a.id,
                a.date.strftime("%Y-%m-%d %H:%M:%S") if a.date else "",
                a.time.strftime("%H:%M:%S") if a.time else "",
                a.service_type,
                a.status,
                a.patient_id,
                a.professional_id
            ])
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=appointments.csv"})

    return appointments


""" 
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info("Consulta SQL: %s", str(query.statement.compile(compile_kwargs={"literal_binds": True}))) """
