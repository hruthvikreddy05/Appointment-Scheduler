from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
import models
from database import engine, get_db
from reminder_service import check_and_send_6hr_reminders

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()
scheduler.add_job(check_and_send_6hr_reminders, 'interval', minutes=5)
scheduler.start()

class Appointment(BaseModel):
    name: str
    email: str
    date: str
    time: str
    reason: str

@app.post("/appointments")
def create_appointment(appointment: Appointment, db: Session = Depends(get_db)):
    db_appointment = models.AppointmentDB(
        name=appointment.name,
        email=appointment.email,
        date=appointment.date,
        time=appointment.time,
        reason=appointment.reason,
        reminder_sent=0
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return {"message": "Appointment scheduled successfully!", "data": db_appointment}

@app.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    return {"appointments": db.query(models.AppointmentDB).all()}

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.AppointmentDB).filter(models.AppointmentDB.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return {"message": f"Appointment #{appointment_id} deleted successfully"}
