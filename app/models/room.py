from datetime import datetime

from sqlalchemy import Column, Integer, String, Float,DateTime
from sqlalchemy.orm import relationship
from app.db import Base

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    bookings = relationship('Booking', back_populates='room', cascade='all, delete-orphan')