import itertools

import redis.asyncio as redis


class DB:

    def __init__(self):
        self.client = redis.Redis()

    async def update_data(self, data: dict) -> None:
        rates = {}
        for key, value in data['rates'].items():
            rates['RUB_' + key] = value
            rates[key + '_RUB'] = round(1 / value, 7)

        for i in itertools.combinations(data['rates'].keys(), r=2):
            for a, b in (i, i[::-1]):
                rates[a + '_' + b] = rates[a + '_RUB'] * rates['RUB_' + b]
        print(rates)
