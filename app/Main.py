from fastapi import FastAPI
from app.api.TtsApi import router as ttsRouter

class MainApplication:
    def __init__(self):
        self.app = FastAPI()
        self.registerRoutes()

    def registerRoutes(self):
        self.app.include_router(ttsRouter)

    def getApp(self):
        return self.app


mainApplication = MainApplication()
app = mainApplication.getApp()