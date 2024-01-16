# Here class helps to connect to DB
class Config:
    DB_URL = "postgresql+asyncpg://postgres:pass@localhost:5432/contact"

config = Config