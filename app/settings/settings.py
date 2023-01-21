import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_USER = os.getenv("POSTGRES_USER")
DB_NAME = os.getenv("POSTGRES_DB")
URL_DB = os.getenv("URL_DB")

POSTGRE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{URL_DB}:5432/{DB_NAME}"

engine = create_engine(POSTGRE_URL)
app = FastAPI()

Base = declarative_base()
db_session = sessionmaker(bind=engine)
session = Session(bind=engine)
