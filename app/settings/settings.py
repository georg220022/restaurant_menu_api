import os

from dotenv import load_dotenv
from fastapi import FastAPI
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_USER = os.getenv("POSTGRES_USER")
DB_NAME = os.getenv("POSTGRES_DB")
URL_DB = os.getenv("URL_DB")
REDIS_PASS = os.getenv("REDIS_PASS")
REDIS_HOST = os.getenv("REDIS_HOST")

REDIS_URL = f"redis://{REDIS_HOST}:6379/0"
POSTGRE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{URL_DB}:5432/{DB_NAME}"

engine = create_engine(POSTGRE_URL)
app = FastAPI()

Base = declarative_base()
cache_redis = Redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
db_session = sessionmaker(bind=engine)
session = Session(bind=engine)
