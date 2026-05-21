from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")

PRICE_SCRAPPER_ENDPOINT = env.str(
    "PRICE_SCRAPPER_ENDPOINT", default="http://localhost:8001"
)
