from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import booking as schemas
from app.models.booking import Booking
from app.db import get_db
from app.crud import booking as crud_booking

router = APIRouter()

@router.post("/create", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud_booking.create_booking(db=db, booking=booking)

@router.delete("/{booking_id}", response_model=schemas.Booking)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud_booking.delete_booking(db=db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.get("/", response_model=list[schemas.Booking])
def read_bookings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_booking.get_booking(db=db, skip=skip, limit=limit)

