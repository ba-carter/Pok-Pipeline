from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.config import Config
from data_models.models import Base

engine = create_engine(
    f"postgresql+psycopg2://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@"
    f"{Config.POSTGRES_HOST}:{Config.POSTGRES_PORT}/{Config.POSTGRES_DB}",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections every hour
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionScoped = scoped_session(SessionLocal)

def get_database_engine():
    return engine

def create_database_session():
    return SessionScoped()

def create_tables(engine_param=None):
    Base.metadata.create_all(bind=engine_param or engine)
