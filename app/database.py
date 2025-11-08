"""
Database setup and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config

# Create database engine
engine = create_engine(
    Config.DATABASE_URL,
    echo=Config.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create scoped session for thread safety
db_session = scoped_session(SessionLocal)

# Base class for all models
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Initialize database - create all tables"""
    # Import all models here to ensure they are registered
    from app.models.user import User
    from app.models.profile import Profile
    from app.models.trip import Trip
    from app.models.pattern import Pattern
    
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")


def get_db():
    """Get database session - use with context manager"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def drop_all():
    """Drop all tables - USE WITH CAUTION!"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️ All tables dropped!")
