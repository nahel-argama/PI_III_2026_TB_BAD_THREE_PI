import environ

env = environ.Env()

env.read_env()

PRICE_SCRAPPER_ENDPOINT = env.str(
    "PRICE_SCRAPPER_ENDPOINT", default="http://localhost:8001"
)
