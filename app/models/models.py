from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
import enum

# Roles posibles para los usuarios
class UserRole(str, enum.Enum):
    admin = "admin"
    profesional = "profesional"
    recepcionista = "recepcionista"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    appointments = relationship("Appointment", back_populates="professional")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(DateTime)
    contact_info = Column(String)

    appointments = relationship("Appointment", back_populates="patient")

class AppointmentStatus(str, enum.Enum):
    pendiente = "pendiente"
    confirmada = "confirmada"
    cancelada = "cancelada"
    reprogramada = "reprogramada"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    time = Column(DateTime, nullable=False)
    service_type = Column(String, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pendiente)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    professional_id = Column(Integer, ForeignKey("users.id"))

    patient = relationship("Patient", back_populates="appointments")
    professional = relationship("User", back_populates="appointments")
