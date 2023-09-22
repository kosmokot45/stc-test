from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config import settings
from core.models import Base, database
from api import router as crud_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=crud_router, prefix=settings.api_prefix)


@app.get("/")
async def main_view():
    return {"message": "hello stc"}
