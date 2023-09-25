from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import async_scoped_session

from app.core.config import settings
# from
# from core.init_db import init_db


class Database:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.db_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_db(self):
        db = async_scoped_session(
            session_factory=self.db_factory,
            scopefunc=current_task
        )
        return db

    async def db_dependency(self) -> AsyncSession:
        async with self.db_factory() as db:
            yield db
            await db.close()

    async def scoped_db_dependency(self) -> AsyncSession:
        db = self.get_scoped_db()
        yield db
        await db.close()


database = Database(url=settings.db_url, echo=settings.db_echo)
