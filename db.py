import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

def get_engine():
    database_url = os.getenv("DATABASE_URL")
    print("DB URL at engine creation:", database_url)
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
