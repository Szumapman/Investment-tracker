from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo_pool=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Create a database session.

    Yields:
        SessionLocal: A database session.
    Exceptions:
        Exception: If an error occurs during the database session.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        # todo: log error
        db.rollback()
    finally:
        db.close()
