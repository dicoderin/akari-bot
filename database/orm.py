from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config import Config
from database.orm_base import Base

DB_LINK = Config('db_path')

class DBSession:
    def __init__(self):
        self.engine = create_engine(DB_LINK, isolation_level="READ UNCOMMITTED")
        self.Session = sessionmaker(bind=self.engine)

    @property
    def session(self):
        return self.Session()

    def create(self):
        Base.metadata.create_all(bind=self.engine, checkfirst=True)


class AsyncDBSession(DBSession):
    def __init__(self):
        self.engine = create_async_engine(DB_LINK, isolation_level="READ UNCOMMITTED")
        self.Session = async_sessionmaker(bind=self.engine)

    async def session(self):
        return self.Session()

Session = DBSession()
async_session = AsyncDBSession()
