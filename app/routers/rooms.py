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

# @router.get("/", response_model=list[HotelRoom])
# def read_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return db.query(Room).offset(skip).limit(limit).all()
#
# @router.delete("/{room_id}", response_model=HotelRoom)
# def delete_room(room_id: int, db: Session = Depends(get_db)):
#     db_room = db.query(Room).filter(Room.id == room_id).first()
#     if db_room is None:
#         raise HTTPException(status_code=404, detail="Room not found")
#     db.delete(db_room)
#     db.commit()
#     return db_room
