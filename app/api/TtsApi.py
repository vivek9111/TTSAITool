import shutil
import os
from fastapi import Depends, Query
from fastapi import APIRouter, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse
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

@router.get("/tts/stream")
def streamTts(request: TtsRequest = Depends()):
    # Get a generator that yields PCM chunks as they are synthesized
    pcm_generator = ttsService.streamSpeech(
        request.text,
        request.language,
        request.voiceId
    )

    # Audio service now processes chunks as they arrive
    stream = audioService.wav_stream(pcm_generator, sample_rate=16000)

    return StreamingResponse(
            stream,
            media_type="audio/wav",
            headers={
                "Content-Type": "audio/wav",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
    )


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
        if len(request.text) > 300:
            raise HTTPException(400, "Text too long")

        filePath = voiceCloningService.cloneVoiceFromId(
            request.voiceId,
            request.text
        )

        return FileResponse(filePath, media_type="audio/wav")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Voice ID not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/clone/stream")
async def cloneVoice(request: CloneRequest = Depends()):
    try:
        # Get the generator that yields audio chunks sentence-by-sentence
        pcm_generator = voiceCloningService.cloneVoiceStreaming(
            request.voiceId,
            request.text,
            language="hi" # Or request.language if provided
        )

        # Use the AudioService to wrap PCM in a WAV container
        # IMPORTANT: XTTS v2 uses 24000Hz, unlike MMS which uses 16000Hz
        stream = audioService.wav_stream(pcm_generator, sample_rate=24000)

        return StreamingResponse(
            stream,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "inline; filename=clone_tts.wav",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            },
        )

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Voice ID not found.")
    except Exception as e:
        print(f"Streaming Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    
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

            for chunk in audioService.wav_stream_speech(pcm):
                # WebSockets send bytes directly
                await ws.send_bytes(chunk)

            # Signal end-of-audio
            await ws.send_text("__END__")

    except WebSocketDisconnect:
        pass