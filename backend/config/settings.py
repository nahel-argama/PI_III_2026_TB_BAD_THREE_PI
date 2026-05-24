from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

PRICE_SCRAPPER_ENDPOINT = env.str(
    "PRICE_SCRAPPER_ENDPOINT", default="http://localhost:8001"
)
ENABLE_DEFAULT_IMAGE_GENERATION = env.bool(
    "ENABLE_DEFAULT_IMAGE_GENERATION", default=False
)
AI_KEY = env.str("AI_KEY", default="")
