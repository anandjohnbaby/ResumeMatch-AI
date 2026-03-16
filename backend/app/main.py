import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes.analyze import router

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running."}

app.mount("/", StaticFiles(directory=os.path.normpath(settings.FRONTEND_DIR), html=True), name="frontend")
