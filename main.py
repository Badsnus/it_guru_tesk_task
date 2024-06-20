import asyncio
import json

import aiohttp
from fastapi import FastAPI, Query
from fastapi_utils.tasks import repeat_every

from config import API_URL
from db import DB

app = FastAPI()
db = DB()


@app.on_event('startup')
@repeat_every(seconds=60 * 60)  # 1 hour
async def update_rates() -> None:
    async with aiohttp.ClientSession() as session:
        while (response := await session.get(API_URL)).status != 200:
            await asyncio.sleep(10)

        data = json.loads(await response.text())
        await db.update_rates(data)


@app.get('/api/rates')
def get_exchange_rate(from_currency: str = Query(alias='from'),
                      to_currency: str = Query(alias='to'),
                      value: float = Query()):
    return {

    }
