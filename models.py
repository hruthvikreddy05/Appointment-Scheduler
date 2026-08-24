from sqlalchemy import Column, Integer, String
from database import Base

class AppointmentDB(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String)
    date = Column(String)
    time = Column(String)
    reason = Column(String)
    reminder_sent = Column(Integer, default=0)
