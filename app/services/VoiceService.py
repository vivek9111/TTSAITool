import os
import shutil
import uuid

class VoiceService:
    """
    Service for managing voice files. This service provides methods to register new voice files and retrieve existing ones by their unique voice ID.
    The registerVoice() method takes a file path to a WAV file, generates a unique voice ID, and stores the file in a designated directory with the voice ID as its name. It returns the generated voice ID.
    The getVoiceFile() method takes a voice ID and returns the file path to the corresponding WAV file.
    """

    def __init__(self):
        self.voiceDir = "voices"
        os.makedirs(self.voiceDir, exist_ok=True)

    def registerVoice(self, filePath):
        """ 
        Registers a new voice file and returns the generated voice ID.
        """

        voiceId = str(uuid.uuid4())
        newPath = os.path.join(self.voiceDir, f"{voiceId}.wav")

        shutil.move(filePath, newPath)

        return voiceId

    def getVoiceFile(self, voiceId):
        """ 
        Retrieves the file path for a given voice ID. Raises FileNotFoundError if the file does not exist.
        """
        path = os.path.join(self.voiceDir, f"{voiceId}.wav")

        if not os.path.exists(path):
            raise FileNotFoundError()

        return path