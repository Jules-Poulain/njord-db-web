from sqlalchemy import Column, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database import Base


class BoatData(Base):
    __tablename__ = "boat_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow)

    lat = Column(Float)
    lon = Column(Float)

    sog = Column(Float)
    cog = Column(Float)

    stw = Column(Float)
    heading = Column(Float)

    tws = Column(Float)
    twa = Column(Float)
    twd = Column(Float)
