from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file!")

# DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/notes_db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)



async def get_async_db():
    async with async_session_maker() as session:
        yield session