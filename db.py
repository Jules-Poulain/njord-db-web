import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

def get_engine():
    database_url = os.getenv("DATABASE_URL")
    print("DB URL at engine creation:", database_url)
    return create_engine(database_url)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
