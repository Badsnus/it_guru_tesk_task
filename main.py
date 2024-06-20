import asyncio
import json

import aiohttp
from fastapi import FastAPI, Query, Depends
from fastapi_utils.tasks import repeat_every

from config import API_URL
from db import DB, get_db
from schemas import ExceptionSchema, RateSchema

app = FastAPI()


@app.on_event('startup')
@repeat_every(seconds=60 * 60)  # 1 hour
async def update_rates(db: DB = Depends(get_db)) -> None:
    async with aiohttp.ClientSession() as session:
        while (response := await session.get(API_URL)).status != 200:
            await asyncio.sleep(10)

        data = json.loads(await response.text())
        await db.update_rates(data)


@app.get('/api/rates')
async def get_exchange_rate(from_currency: str = Query(alias='from'),
                            to_currency: str = Query(alias='to'),
                            value: float = Query(),
                            db: DB = Depends(get_db)) -> RateSchema | ExceptionSchema:
    try:
        rate = await db.get_rates(from_currency + '_' + to_currency)
        return RateSchema(rate=rate * value)
    except TypeError:
        return ExceptionSchema(error='Invalid currency')
