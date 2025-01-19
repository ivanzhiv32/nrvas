from collections.abc import Iterator, Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def create_session_maker(db_url: str) -> Callable[[], Iterator[Session]]:
    engine = create_engine(
        db_url,
        echo=False,
        pool_size=15,
        max_overflow=15,
    )
    session_maker = sessionmaker(
        engine,
        autoflush=False,
        expire_on_commit=False
    )

    def transaction() -> Iterator[Session]:
        with session_maker() as session:
            yield session

    return transaction
