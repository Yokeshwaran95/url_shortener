from select import select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from model import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio



class DbManager():
    def __get_engine(self):
        args = dict(echo=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)
        engine = create_engine("sqlite:///./urls.db", **args)
        return engine

    def db_init(self):
        Base.metadata.create_all(bind=self.__get_engine())

    def get_session(self):
        Session = sessionmaker(bind=self.__get_engine())
        with Session() as session:
            return session

    def close_session(self, session):
        session.close()

class ORMHelper():
    def get(self, table_class, **filter):
        where_clause = set()
        if filter is not {}:
            for key, value in filter.items():
                where_clause.add(getattr(table_class, key) == value)
        return DbManager().get_session().query(table_class).filter(*where_clause).all()

    def add(self, table_class, **entries):
        session = DbManager().get_session()
        entry = table_class(**entries)
        session.merge(entry)  # merge will add or update
        session.commit()
        DbManager().close_session(session)
