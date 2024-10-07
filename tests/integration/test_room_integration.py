import pytest
from app.models.room import Room


@pytest.fixture(scope='function')
def sample_room_data():
    return {
        'room_number': '100',
        'description': 'Test description',
        'price': 1000
    }

@pytest.mark.asyncio
async def test_create_room(async_client, db, sample_room_data):
    print(f"Debug: {type(async_client)}!")  # Диагностическое сообщение
    response = await async_client.post("/rooms/", json=sample_room_data)
    assert response.status_code == 201
    room_data = response.json()

    assert room_data['room_number'] == sample_room_data['room_number']
    assert room_data['description'] == sample_room_data['description']
    assert room_data['price'] == sample_room_data['price']

    room = db.query(Room).filter(Room.id == room_data['id']).first()
    assert room is not None
    assert room.room_number == sample_room_data['room_number']
    assert room.description == sample_room_data['description']
    assert room.price == sample_room_data['price']

@pytest.mark.asyncio
async def test_get_room(async_client, sample_room_data):
    create_response = await async_client.post("/rooms/", json=sample_room_data)
    room_data = create_response.json()

    response = await async_client.get(f"/rooms/{room_data['id']}/")
    assert response.status_code == 200
    retrieved_room_data = response.json()

    assert retrieved_room_data['room_number'] == sample_room_data['room_number']
    assert retrieved_room_data['description'] == sample_room_data['description']
    assert retrieved_room_data['price'] == sample_room_data['price']

@pytest.mark.asyncio
async def test_delete_room(async_client, db, sample_room_data):
    create_response = await async_client.post("/rooms/", json=sample_room_data)
    room_data = create_response.json()

    delete_response = await async_client.delete(f"/rooms/{room_data['id']}/")
    assert delete_response.status_code == 200

    room = db.query(Room).filter(Room.id == room_data['id']).first()
    assert room is None