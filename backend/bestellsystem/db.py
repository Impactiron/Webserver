"""Database configuration and setup using SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from bestellsystem.config import Config


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


# Create engine using DATABASE_URL from config
engine = create_engine(
    Config.DATABASE_URL,
    echo=Config.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    """Get a new database session.
    
    Returns:
        SQLAlchemy Session instance
    """
    return SessionLocal()
