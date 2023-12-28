from sqlmodel import Session
from database import engine

# Get session
def get_session():
  with Session(engine) as session:
    yield session