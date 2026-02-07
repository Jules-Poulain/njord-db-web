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

    readings = data["data"]["readings"]

    pos = find_pgn(readings, "129029")
    sogcog = find_pgn(readings, "129026")
    speed = find_pgn(readings, "128259")
    heading_data = find_pgn(readings, "127250")
    wind = find_pgn(readings, "130306")

    if not all([pos, sogcog, speed, heading_data, wind]):
        print("Missing PGNs, skipping")
        return

    lat = pos["Latitude"]
    lon = pos["Longitude"]

    sog = sogcog["SOG"]
    cog = sogcog["COG"]

    stw = speed.get("Speed Water Referenced", 0)

    heading = heading_data["Heading"]

    tws = wind["Wind Speed"]
    twa = wind["Wind Angle"]
    twd = (heading + twa) % 360

    print(f"LAT:{lat} LON:{lon} SOG:{sog} COG:{cog} STW:{stw} HDG:{heading} TWS:{tws} TWA:{twa} TWD:{twd}")

    session = get_session()

    entry = BoatData(
        lat=lat,
        lon=lon,
        sog=sog,
        cog=cog,
        stw=stw,
        heading=heading,
        tws=tws,
        twa=twa,
        twd=twd,
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