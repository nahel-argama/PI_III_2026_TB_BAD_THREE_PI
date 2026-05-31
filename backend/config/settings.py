from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

PRICE_SCRAPPER_ENDPOINT = env.str(
    "PRICE_SCRAPPER_ENDPOINT", default="http://localhost:8001"
)

# AI Stuff
ENABLE_DEFAULT_IMAGE_GENERATION = env.bool(
    "ENABLE_DEFAULT_IMAGE_GENERATION", default=False
)

CF_ACCOUNT_ID = env.str("CF_ACCOUNT_ID", default="")
CF_TOKEN = env.str("CF_TOKEN", default="")
CF_MODEL = env.str("CF_MODEL", default="")
CF_ENDPOINT = env.str("CF_ENDPOINT", default="")
