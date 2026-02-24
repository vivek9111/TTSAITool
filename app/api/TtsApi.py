from fastapi import APIRouter
from app.services.TextService import TextService
from app.services.TtsService import TtsService
from app.services.AudioService import AudioService
from app.schemas.TtsSchema import TtsRequest, TtsResponse

router = APIRouter()

textService = TextService()
ttsService = TtsService()
audioService = AudioService()

@router.get("/health")
def healthCheck():
    return {"status": "Backend is running"}

@router.post("/tts", response_model=TtsResponse)
def generateTts(request: TtsRequest):

    processedText = textService.preprocessText(request.text, request.language)
    audioData = ttsService.generateSpeech(processedText, request.language, request.voiceId)
    audioPath = audioService.saveAudio(audioData)

    return TtsResponse(
        message="TTS generated",
        audioPath=audioPath,
        language=request.language,
        voiceId=request.voiceId
    )