import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.db import Base, get_db
from app.models.room import Room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='function')
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

# @pytest.fixture(scope='module')
# def client():
#     def override_get_db():
#         yield TestingSessionLocal()
#
#     app.dependency_overrides[get_db] = override_get_db
#     with TestClient(app) as client:
#         yield client

@pytest.fixture(scope='module')
async def async_client():
    # Переопределение зависимости get_db на фикстуру с тестовой базой данных
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Создание асинхронного клиента для FastAPI приложения
    async with AsyncClient(app=app, base_url="http://test") as ac:
        print(f"Debug: {type(ac)}")  # Диагностическое сообщение
        yield ac

@pytest.fixture
def create_room(db):
    def _create_room(room_number: str, description: str, price: int):
        room = Room(room_number=room_number, description=description, price=price)
        db.add(room)
        db.commit()
        db.refresh(room)
        return room
    return _create_room