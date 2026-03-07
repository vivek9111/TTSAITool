import os
import shutil
import uuid

class VoiceService:

    def __init__(self):
        self.voiceDir = "voices"
        os.makedirs(self.voiceDir, exist_ok=True)

    def registerVoice(self, filePath):

        voiceId = str(uuid.uuid4())
        newPath = os.path.join(self.voiceDir, f"{voiceId}.wav")

        shutil.move(filePath, newPath)

        return voiceId

    def getVoiceFile(self, voiceId):

        path = os.path.join(self.voiceDir, f"{voiceId}.wav")

        if not os.path.exists(path):
            raise FileNotFoundError()

        return path