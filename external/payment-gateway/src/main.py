from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import api_router
from src.utils.error_handler import validation_exception_handler

app = FastAPI(
    title="Fake Payment Gateway",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(api_router)