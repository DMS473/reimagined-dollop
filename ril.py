from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
import httpx
import validators

from urllib.parse import quote
import xmltodict

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

import time

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    wikidata_by_id_url: str = os.getenv("WIKIDATA_BY_ID_URL")
    wikidata_by_name_url: str = os.getenv("WIKIDATA_BY_NAME_URL")
    ncbi_by_id_url: str = os.getenv("NCBI_BY_ID_URL")
    ncbi_by_name_url: str = os.getenv("NCBI_BY_NAME_URL")
    gbif_by_id_url: str = os.getenv("GBIF_BY_ID_URL")
    gbif_by_name_url: str = os.getenv("GBIF_BY_NAME_URL")
    gbif_by_id_detail_url: str = os.getenv("GBIF_BY_ID_DETAIL_URL")

settings = Settings()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


def pre_process_url(url: str) -> str:
    try:
        result = quote(url, safe=':/?=&')
        result = str(result)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def check_url_valid(url: str) -> bool:
    try:
        if not validators.url(url):
            return False
        return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return settings


    