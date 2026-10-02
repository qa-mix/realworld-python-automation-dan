import os

from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL")

if not BASE_API_URL:
    raise RuntimeError("BASE_API_URL is not set")