import itertools
from typing import AsyncGenerator

import redis.asyncio as redis
from config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT

pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
)


class DB:

    def __init__(self, pool: redis.ConnectionPool) -> None:
        self.client = redis.Redis.from_pool(pool)

    @staticmethod
    def __get_key(from_currency: str, to_currency: str) -> str:
        return from_currency + '_' + to_currency

    async def update_rates(self, data: dict) -> None:
        rates = {}
        for key, value in data['rates'].items():
            rates[self.__get_key('RUB', key)] = value
            rates[self.__get_key(key, 'RUB')] = round(1 / value, 7)

        for a, b in itertools.combinations(data['rates'].keys(), r=2):
            rates[self.__get_key(a, b)] = (
                    rates[self.__get_key(a, 'RUB')] *
                    rates[self.__get_key('RUB', b)]
            )
            rates[self.__get_key(b, a)] = (
                    rates[self.__get_key(b, 'RUB')] *
                    rates[self.__get_key('RUB', a)]
            )

        for key, value in rates.items():
            await self.client.set(key, value)

    async def get_rates(self, from_currency: str, to_currency: str) -> float:
        return float(await self.client.get(self.__get_key(from_currency, to_currency)))


async def get_db() -> AsyncGenerator:
    yield DB(pool)
