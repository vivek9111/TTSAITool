from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.TtsApi import router as ttsRouter
from app.core.ModelRegistry import ModelRegistry
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup running")
    ModelRegistry.loadModels()
    print("=== MODEL LOADED ===")
    yield
    print("Shutdown running")

app = FastAPI(lifespan=lifespan)
app.include_router(ttsRouter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)