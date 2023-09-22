alembic init migrations
alembic revision --autogenerate -m "database creation"
alembic upgrade %version%