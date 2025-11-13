from pydantic import BaseModel, Field
from datetime import date
from datetime import time
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from datetime import date as date_type
from app.models.models import UserRole
from typing import Optional
from pydantic import root_validator
from pydantic import field_validator

class UserCreate(BaseModel):
    name: str
    email: str
    password: str = Field(..., max_length=72)
    role: UserRole

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class AppointmentStatus(str, Enum):
    pendiente = "pendiente"
    confirmada = "confirmada"
    cancelada = "cancelada"
    reprogramada = "reprogramada"

class AppointmentBase(BaseModel):
    date: date
    service_type: str
    patient_id: int
    professional_id: int

class AppointmentCreate(BaseModel):
    date: date
    time: time
    service_type: str
    status: str
    patient_id: int
    professional_id: int


class AppointmentOut(AppointmentBase):
    id: int
    status: AppointmentStatus
    date: datetime  # ✅ acepta fecha con hora

    class Config:
        orm_mode = True
        
class PatientCreate(BaseModel):
    name: str
    birth_date: date
    contact_info: str

class PatientOut(PatientCreate):
    id: int

    @field_validator("birth_date", mode="before")
    @classmethod
    def convert_datetime_to_date(cls, v):
        if isinstance(v, datetime):
            return v.date()
        return v

    class Config:
        from_attributes = True

class PatientUpdate(BaseModel):
    name: Optional[str]
    birth_date: Optional[date]
    contact_info: Optional[str]

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str

class AppointmentFilter(BaseModel):
    date: Optional[date_type] = None
    status: Optional[str] = None  # "pendiente", "confirmada", etc.
    professional_id: Optional[int] = None
    
class WeeklyAgendaFilter(BaseModel):
    start_date: date
    end_date: date
    status: Optional[str] = None
    professional_id: Optional[int] = None
    
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role: Optional[UserRole]
