import os
import io
import struct
import soundfile as sf
import numpy as np

class AudioService:
    def __init__(self):
        self.outputDir = "generated_audio"
        os.makedirs(self.outputDir, exist_ok=True)
    
    def toWavBytes(self, audioArray, sampleRate: int = 16000) -> bytes:
        if audioArray is None or len(audioArray) == 0:
            raise ValueError("Empty audio array")

        audioArray = np.asarray(audioArray)

        buffer = io.BytesIO()
        sf.write(buffer, audioArray, sampleRate, format="WAV")
        buffer.seek(0)

        return buffer.read()
    
    def wav_stream(self, pcm: np.ndarray, sample_rate: int = 16000, chunk_size: int = 4096):
        pcm = np.clip(pcm, -1.0, 1.0)
        pcm16 = (pcm * 32767).astype(np.int16)

        # WAV header with unknown length
        header = self._wav_header(sample_rate)
        yield header

        for i in range(0, len(pcm16), chunk_size):
            yield pcm16[i:i+chunk_size].tobytes()

    def _wav_header(self, sample_rate):
        return struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF",
            0xFFFFFFFF,
            b"WAVE",
            b"fmt ",
            16,
            1,
            1,
            sample_rate,
            sample_rate * 2,
            2,
            16,
            b"data",
            0xFFFFFFFF,
        )