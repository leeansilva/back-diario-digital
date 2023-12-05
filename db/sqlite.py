
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlmodel import create_engine, Session
from typing import Union, Optional

SQLITE = 'sqlite:///db/data/data.db'
# Conexion sincronica
engine = create_engine(SQLITE)

def CrearTablas():
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session
