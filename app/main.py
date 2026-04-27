from fastapi import FastAPI
from app.api.router import api_router

from app.core.config import settings  # imported for startup validation

app = FastAPI()

app.include_router(api_router)
