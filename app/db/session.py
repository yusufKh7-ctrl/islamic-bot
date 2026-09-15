from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set!")

engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=0,
    connect_args={"ssl": "require"},
)

async_session = async_sessionmaker(engine, expire_on_commit=False)