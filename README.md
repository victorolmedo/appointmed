# 📅 Sistema de Gestión de Citas Médicas

Este proyecto es una API REST construida con FastAPI para gestionar citas médicas, pacientes, profesionales y usuarios con autenticación JWT y control de roles.

---

## 🚀 Características principales

- Registro de citas con validaciones de superposición y duplicado
- Filtro de agenda diaria y semanal por profesional
- Exportación de citas a CSV
- Autenticación JWT con roles (`admin`, `recepcionista`, `profesional`)
- CRUD completo de usuarios
- Documentación Swagger automática

---

## 🧱 Estructura del proyecto

---

## 🔐 Roles y permisos

| Rol           | Acceso a endpoints                      |
|---------------|------------------------------------------|
| admin         | CRUD completo, ver todas las citas       |
| recepcionista | Crear citas, ver agendas                 |
| profesional   | Ver su propia agenda                     |

---

## 🛠️ Instalación

```bash
git clone https://github.com/tuusuario/appointed.git
cd appointed
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
uvicorn app.main:app --reload


📦 Endpoints útiles
POST /auth/login → Login con JWT

POST /appointments/ → Crear cita

POST /appointments/agenda → Ver agenda diaria

POST /appointments/agenda/semana → Ver agenda semanal

GET /appointments/agenda/all → Ver todas las citas (admin)

GET /appointments/agenda/all?export_csv=true → Exportar citas a CSV

