import asyncio
from njordlink_query import get_latest_pgns
from db import Session, BoatData
import uuid

async def collect():
    data = await get_latest_pgns()

    session = Session()

    readings = data["readings"]

    entry = BoatData(
        id=str(uuid.uuid4()),
        lat=readings["position"]["lat"],
        lng=readings["position"]["lng"],
        sog=readings["sog"],
        cog=readings["cog"],
        pgns=readings
    )

    session.add(entry)
    session.commit()
    session.close()

if __name__ == "__main__":
    asyncio.run(collect())