from pydantic import BaseModel
from datetime import date

class BookingBase(BaseModel):
    room_id: int
    date_start: date
    date_end: date

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int

    class Config:
        from_attributes = True
