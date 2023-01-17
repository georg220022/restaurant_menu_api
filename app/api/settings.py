from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker, Session

POSTGRE_URL = "postgresql+psycopg2://gera:gera@postgres_db:5432/restaurant_menu"

engine = create_engine(POSTGRE_URL)
app = FastAPI()

Base = declarative_base()
db_session = sessionmaker(bind=engine)
session = Session(bind=engine)
