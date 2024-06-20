import itertools

import redis.asyncio as redis


class DB:

    def __init__(self):
        self.client = redis.Redis()

    async def update_rates(self, data: dict) -> None:
        rates = {}
        for key, value in data['rates'].items():
            rates['RUB_' + key] = value
            rates[key + '_RUB'] = round(1 / value, 7)

        for a, b in itertools.combinations(data['rates'].keys(), r=2):
            rates[a + '_' + b] = rates[a + '_RUB'] * rates['RUB_' + b]
            rates[b + '_' + a] = rates[b + '_RUB'] * rates['RUB_' + a]

        for key, value in rates:
            await self.client.set(key, value)
