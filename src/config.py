import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_HOST = os.getenv('REDIS_HOST')
