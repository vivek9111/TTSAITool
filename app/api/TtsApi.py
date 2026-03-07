import shutil
import os
from fastapi import APIRouter, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from app.services.TextService import TextService
from app.services.TtsService import TtsService
from app.services.AudioService import AudioService
from app.schemas.TtsSchema import TtsRequest, CloneRequest
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.VoiceService import VoiceService
from app.services.VoiceCloningService import VoiceCloningService


router = APIRouter()
textService = TextService()
voiceService = VoiceService()
ttsService = TtsService()
audioService = AudioService()
voiceCloningService = VoiceCloningService()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.get("/health")
def healthCheck():
    return {"status": "Backend is running"}

@router.post("/tts")
def generateTts(request: TtsRequest):
    audioArray = ttsService.generateSpeech(
        request.text,
        request.language,
        request.voiceId
    )

    audioBytes = audioService.toWavBytes(audioArray)

    return Response(
        content=audioBytes,
        media_type="audio/wav",
        headers={
            "Content-Disposition": "inline; filename=tts.wav",
            "Content-Length": str(len(audioBytes))
        }
    )

@router.post("/tts/stream")
def streamTts(request: TtsRequest):
    pcm = ttsService.streamSpeech(
        request.text,
        request.language,
        request.voiceId
    )

    stream = audioService.wav_stream(pcm)

    return StreamingResponse(
        stream,
        media_type="audio/wav",
        headers={
            "Content-Disposition": "inline; filename=tts.wav",
            "Cache-Control": "no-cache",
        },
    )

@router.websocket("/ws/tts")
async def websocketTts(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            payload = await ws.receive_json()

            text = payload.get("text", "")
            language = payload.get("language", "hi")
            voiceId = payload.get("voiceId", "default")

            pcm = ttsService.streamSpeech(text, language, voiceId)

            for chunk in audioService.wav_stream(pcm):
                # WebSockets send bytes directly
                await ws.send_bytes(chunk)

            # Signal end-of-audio
            await ws.send_text("__END__")

    except WebSocketDisconnect:
        pass

@router.post("/voices/register")
async def registerVoice(file: UploadFile = File(...)):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only WAV files supported.")

    tempPath = os.path.join(TEMP_DIR, file.filename)

    try:
        with open(tempPath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        voiceId = voiceService.registerVoice(tempPath)

        return {"voiceId": voiceId}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(tempPath):
            os.remove(tempPath)

@router.post("/clone")
async def cloneVoice(request: CloneRequest):
    try:
        audioBytes = voiceCloningService.cloneVoiceFromId(
            request.voiceId,
            request.text
        )

        return Response(content=audioBytes, media_type="audio/wav")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Voice ID not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))