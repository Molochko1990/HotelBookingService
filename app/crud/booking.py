from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate


def create_booking(db: Session, booking: BookingCreate):
    db_booking = Booking(
        room_id=booking.room_id,
        date_start=booking.date_start,
        date_end=booking.date_end)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
    return db_booking

def get_booking(db: Session, skip: int = 0, limit: int = 10):
    bookings = db.query(Booking).offset(skip).limit(limit).all()
    return bookings