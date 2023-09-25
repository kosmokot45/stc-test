## Alembic part
```
alembic init migrations
alembic revision --autogenerate -m "database creation"
alembic upgrade %version%
```
## Run part
{} - means optional
```
python -m venv venv
.\venv\Scripts\activate
{pip install poetry}
poetry install
uvicorn app.main:app {--reload}
```