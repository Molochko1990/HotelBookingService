from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room import HotelRoomCreate


def create_room(db: Session, room: HotelRoomCreate):
    db_room = Room(
        room_number=room.room_number,
        description=room.description,
        price=room.price)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: int):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if db_room:
        db.delete(db_room)
        db.commit()
    return db_room


def get_rooms(db: Session, skip: int = 0, limit: int = 10, sort_by: str = None, order: str = "asc"):
    query = db.query(Room)

    if sort_by == "price":
        query = query.order_by(Room.price if order == "asc" else Room.price.desc())
    elif sort_by == "created_at":
        query = query.order_by(Room.created_at if order == "asc" else Room.created_at.desc())

    return query.offset(skip).limit(limit).all()
