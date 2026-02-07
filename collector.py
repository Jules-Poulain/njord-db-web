print("Collector.py started")

import asyncio
from njordlink_query import get_latest_pgns
from db import get_session
from models import BoatData
import uuid


def find_pgn(readings, prefix):
    for k, v in readings.items():
        if k.startswith(prefix):
            return v
    return None


async def collect():
    data = await get_latest_pgns()

    if not data:
        print("No data from Njord")
        return

    print("RAW VIAM DATA:", data)

    readings = data["data"]

    session = get_session()

    entry = BoatData(
        lat=readings.get("lat"),
        lng=readings.get("lng"),
        sog=readings.get("sog"),
        cog=readings.get("cog"),
        boatspeed=readings.get("boatspeed"),
        heading=readings.get("heading"),
        tws=readings.get("tws"),
        twa=readings.get("twa"),
        twd=readings.get("twd"),
        raw=readings
    )

    session.add(entry)
    session.commit()
    session.close()


async def loop_collect():
    while True:
        try:
            await collect()
        except Exception as e:
            print("Collector error:", e)

        await asyncio.sleep(60)  # collect every 60 seconds

if __name__ == "__main__":
    import time
    print("Name loop entered")
    while True:
        print("Data collection in progress...")
        asyncio.run(loop_collect())
        time.sleep(1)
else:
    print("Main loop not entered")