from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.config import config

app = FastAPI(
    title=config.get("app_name", "Fake News Detector API"),
    version=config.get("version", "1.0.0"),
    description="Backend API for Fake News Detection using ML and LLM",
)

cors_origins = config.get("api", {}).get("cors_origins", ["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": "Fake News Detector API",
        "version": config.get("version", "1.0.0"),
        "status": "running",
    }