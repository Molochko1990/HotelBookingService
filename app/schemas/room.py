from datetime import datetime

from pydantic import BaseModel

class HotelRoomBase(BaseModel):
    room_number: str
    description: str
    price: int

class HotelRoomCreate(HotelRoomBase):
    pass

class HotelRoom(HotelRoomBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
