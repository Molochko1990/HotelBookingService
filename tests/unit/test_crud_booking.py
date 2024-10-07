import pytest
from app.crud.booking import create_booking, get_booking, delete_booking
from app.models.booking import Booking
from app.schemas.booking import BookingCreate


@pytest.fixture
def sample_booking_data(create_room):
    room = create_room(room_number="Test Room", description="Test Description", price=1000)
    return {
        'room_id':room.id,
        'date_start':'2025-10-01',
        'date_end':'2025-10-05'
    }

def test_create_booking(db, sample_booking_data):
    BookingCreateModel = BookingCreate(**sample_booking_data)
    result = create_booking(db, BookingCreateModel)

    assert result.room_id == BookingCreateModel.room_id
    assert result.date_start == BookingCreateModel.date_start
    assert result.date_end == BookingCreateModel.date_end

    booking_in_db = db.query(Booking).filter(Booking.id == result.id).first()
    assert booking_in_db is not None

def test_delete_booking(db, sample_booking_data):
    BookingCreateModel = BookingCreate(**sample_booking_data)
    new_booking = create_booking(db, BookingCreateModel)

    result = delete_booking(db, new_booking.id)

    assert result is not None
    assert result.id == new_booking.id

    booking_in_db = get_booking(db)
    assert all(booking.id != new_booking.id for booking in booking_in_db)


def test_get_booking(db, sample_booking_data):
    BookingCreateModel = BookingCreate(**sample_booking_data)
    new_booking = create_booking(db, BookingCreateModel)

    result = get_booking(db)

    assert result is not None
    assert result == [new_booking]