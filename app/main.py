from fastapi import FastAPI, HTTPException
from routers import portal_router, raw_data_router
import uvicorn
from config import HOST, PORT

app = FastAPI()

app.include_router(portal_router.router, prefix="/portals", tags=["portals"])
app.include_router(raw_data_router.router, prefix="/raws", tags=["raws"])

if __name__ == "__main__":
    try:
        uvicorn.run(app, host=HOST, port=int(PORT))

    except Exception as e:
        raise Exception(f"An error occurred while running the app: {str(e)}")