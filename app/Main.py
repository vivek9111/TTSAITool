from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.TtsApi import router as ttsRouter
from app.core.ModelRegistry import ModelRegistry

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup running")
    ModelRegistry.loadModels()
    print("=== MODEL LOADED ===")
    yield
    print("Shutdown running")

app = FastAPI(lifespan=lifespan)
app.include_router(ttsRouter)