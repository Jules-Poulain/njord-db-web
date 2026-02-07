from database import Base
from db import engine
import models

Base.metadata.create_all(engine)

from fastapi import FastAPI
from njordlink_query import get_latest_pgns

app = FastAPI()

@app.get("/boat")
async def boat_data():
    data = await get_latest_pgns()
    return data


# This part is ONLY for running locally (optional but clean)
if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port)
