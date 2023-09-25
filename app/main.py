from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.models import Base
from app.core.models import database
from app.core.init_db import init_db
from app.api import router as api_router


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
