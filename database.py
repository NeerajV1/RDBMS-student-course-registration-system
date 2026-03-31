import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

load_dotenv()

# echo=True prints the SQL commands to your terminal for every action
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)