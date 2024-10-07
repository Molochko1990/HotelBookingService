from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.db import get_db, engine, Base
from app.routers import rooms, bookings
from app.models.room import Room
from app.models.booking import Booking



app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Catalog API"}

app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()