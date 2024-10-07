from sys import modules

import pytest

from app.crud.room import create_room, get_rooms, delete_room
from app.models.room import Room
from app.schemas.room import HotelRoomCreate


@pytest.fixture
def sample_room_data():
    return {
        'room_number': '100',
        'description': 'Test description',
        'price': 1000
    }


def test_create_room(db, sample_room_data):
    RoomModel = HotelRoomCreate(**sample_room_data)
    result = create_room(db, RoomModel)

    assert result is not None
    assert result.room_number == RoomModel.room_number
    assert result.price == RoomModel.price

    room_in_db = db.query(Room).filter(Room.id == result.id).first()
    assert room_in_db is not None

def test_delete_room(db, sample_room_data):
    RoomModel = HotelRoomCreate(**sample_room_data)
    new_room = create_room(db, RoomModel)

    result = delete_room(db, new_room.id)

    assert result is not None
    assert result.id == new_room.id

    room_in_db = get_rooms(db)

    assert all(room.id != new_room.id for room in room_in_db)

def test_get_rooms(db, sample_room_data):
    RoomModel = HotelRoomCreate(**sample_room_data)
    new_room = create_room(db, RoomModel)

    assert new_room is not None

    result = get_rooms(db)
    assert result == [new_room]
