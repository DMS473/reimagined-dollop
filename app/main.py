from fastapi import FastAPI, HTTPException
from routers import portal_router, raw_data_router

app = FastAPI()

app.include_router(portal_router.router, prefix="/portals", tags=["portals"])
app.include_router(raw_data_router.router, prefix="/raw", tags=["raw"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
