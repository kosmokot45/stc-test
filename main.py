from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from core.config import settings
from core.models import Base, database
from api import router as api_router
from core.init_db import init_db

from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as db:
        # await db.run_sync(Base.metadata.drop_all)
        await db.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router, prefix=settings.api_prefix)


@app.get("/")
async def main_view():
    return {"message": "hello stc"}


@app.post("/init")
async def init_db_data(db: AsyncSession = Depends(database.scoped_db_dependency)):
    await init_db(db=db)
