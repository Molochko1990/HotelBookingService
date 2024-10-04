from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room import HotelRoom, HotelRoomCreate
from app.db import get_db
from app.crud import room as crud_room

router = APIRouter()

@router.post("/", response_model=HotelRoom)
def create_room(room: HotelRoomCreate, db: Session = Depends(get_db)):
    return crud_room.create_room(db, room)


@router.delete("/{room_id}", response_model=HotelRoom)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud_room.delete_room(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


@router.get("/", response_model=list[HotelRoom])
def read_rooms(skip: int = 0, limit: int = 10, sort_by: str = None, order: str = 'asc', db: Session = Depends(get_db)):
    return crud_room.get_rooms(db=db, skip=skip, limit=limit, sort_by=sort_by, order=order)
