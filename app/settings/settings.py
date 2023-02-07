import os

from dotenv import load_dotenv
from fastapi import FastAPI
from redis import asyncio as aredis
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

load_dotenv()


DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_USER = os.getenv("POSTGRES_USER")
DB_NAME = os.getenv("POSTGRES_DB")
URL_DB = os.getenv("URL_DB")
REDIS_PASS = os.getenv("REDIS_PASS")
REDIS_HOST = os.getenv("REDIS_HOST")


REDIS_URL = f"redis://{REDIS_HOST}:6379/0"
POSTGRE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{URL_DB}:5432/{DB_NAME}"


engine = create_async_engine(
    POSTGRE_URL, echo=False, pool_pre_ping=True, poolclass=NullPool
)
eng_celery = create_engine(POSTGRE_URL)

cache_redis = aredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
db_async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    bind=engine,
    expire_on_commit=False,
)

app = FastAPI()
