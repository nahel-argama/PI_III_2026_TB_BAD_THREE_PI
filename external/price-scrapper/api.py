from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Price Scraper", version="0.1.0")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Price Scraper API", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
