from fastapi import FastAPI, HTTPException
from routers import item_router, portal_router

app = FastAPI()

app.include_router(item_router.router, prefix="/items", tags=["items"])
app.include_router(portal_router.router, prefix="/portals", tags=["portals"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
