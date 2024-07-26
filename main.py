from fastapi import FastAPI, Request
import httpx

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

import time

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    wikidata_by_id_url: str = os.getenv("WIKIDATA_BY_ID_URL")

settings = Settings()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/wikidata")
async def get_wikidata_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.wikidata_by_id_url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
    return data