import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_SQLALCHEMY_DATABASE_URL = os.getenv('TEST_DATABASE_URL')

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='module')
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='module')
def client():
    def override_get_db():
        yield TestingSessionLocal()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
