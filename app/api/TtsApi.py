from fastapi import APIRouter, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from app.services.TextService import TextService
from app.services.TtsService import TtsService
from app.services.AudioService import AudioService
from app.schemas.TtsSchema import TtsRequest


router = APIRouter()

textService = TextService()
ttsService = TtsService()
audioService = AudioService()

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