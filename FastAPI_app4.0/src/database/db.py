import contextlib
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from src.conf.config import config

#This structure allows you to use the get_db function as a dependency in your FastAPI routes or functions, 
#ensuring that each request gets a separate database session and the session is properly managed 
#(committed or rolled back) based on the success or failure of the request.

class DataBaseSessionManager:
    def __init__(self, url: str) -> None:
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False, bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as error:
            print(error)
            await session.rollback()
        finally:
            await session.close()

sessionmanager = DataBaseSessionManager(config.SQLALCHEMY_DATABASE_URL)

async def get_db():
    async with sessionmanager.session() as session:
        yield session
