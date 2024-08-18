from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import portal_router, raw_data_router, term_router
import uvicorn
from config import HOST, PORT

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(portal_router.router, prefix="/portals", tags=["portals"])
app.include_router(raw_data_router.router, prefix="/raws", tags=["raws"])
app.include_router(term_router.router, prefix="/terms", tags=["terms"])

if __name__ == "__main__":
    try:
        uvicorn.run(app, host=HOST, port=int(PORT))

    except Exception as e:
        raise Exception(f"An error occurred while running the app: {str(e)}")