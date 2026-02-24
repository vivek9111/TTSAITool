import soundfile as sf
import os
import uuid

class AudioService:
    def __init__(self):
        self.outputFolder = "output"
        os.makedirs(self.outputFolder, exist_ok=True)

    def saveAudio(self, audioArray):
        fileName = f"{uuid.uuid4()}.wav"
        filePath = os.path.join(self.outputFolder, fileName)

        sf.write(filePath, audioArray, 16000)
        print(audioArray.shape, audioArray.dtype)
        
        return filePath
    

