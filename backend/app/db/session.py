from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core import config

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    # TODO: configure as part of scaling work
    pool_size=10,
    max_overflow=240,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def make_declarative_base():
    Base = declarative_base()

    Base.metadata.naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s__%(column_0_name)s",
        "ck": "ck_%(table_name)s__%(constraint_name)s",
        "fk": "fk_%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    # overwrite the SQLAlchemy __repr__ method for ORM instances
    def base_repr(self):
        values = [
            f"{col.key}={repr(getattr(self, col.key))}" for col in self.__table__.c
        ]
        return f'<Row of {self.__tablename__}: {", ".join(values)}>'

    Base.__repr__ = base_repr
    return Base


Base = make_declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: Update to async db connection
# https://fastapi.tiangolo.com/advanced/async-sql-databases/
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session
#         await session.commit()
#
# class DB(AsyncSession):
#     def __new__(cls,db:AsyncSession = Depends(get_session)):
#         return db
#
# # in the route:
# @app.post("/my-route/")
# async def do_something(db: DB = Depends()): ...
