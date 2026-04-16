from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.api.router import api_router
from src.utils.error_handler import validation_exception_handler

app = FastAPI(
    title="Fake Payment Gateway",
    version="0.1.0",
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(api_router)