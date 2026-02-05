from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime
import datetime

Base = declarative_base()

class BoatData(Base):
    __tablename__ = "boat_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    heading = Column(Float)
