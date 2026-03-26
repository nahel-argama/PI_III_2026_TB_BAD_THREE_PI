from fastapi import FastAPI

from app.api import router
import app.env as env

app = FastAPI(title="Price Scraper", version="0.1.0")

app.include_router(router)


@app.get("/health")
def root():
    return {"message": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=env.API_HOST, port=env.API_PORT)
