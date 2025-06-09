from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


def get_database_engine():
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")

    connection_string = (
        f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )
    return create_engine(connection_string, pool_pre_ping=True)


def create_database_session():
    engine = get_database_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def create_tables(engine):
    from data_models.models import Base

    Base.metadata.create_all(bind=engine)
