from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def create_session_maker(db_url: str) -> sessionmaker:
    engine = create_engine(
        db_url,
        echo=False,
        pool_size=15,
        max_overflow=15,
    )
    return sessionmaker(
        engine,
        autoflush=False,
        expire_on_commit=False
    )


def get_session(session_maker: sessionmaker) -> Iterator[Session]:
    with session_maker() as session:
        yield session
