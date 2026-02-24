from pydantic import BaseModel

class TtsRequest(BaseModel):
    text: str
    language: str = "hi"
    voiceId: str = "default"

class TtsResponse(BaseModel):
    message: str
    audioPath: str
    language: str
    voiceId: str


    