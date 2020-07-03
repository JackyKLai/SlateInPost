import speech_recognition as sr
import time
import os


class Sr:
    def __init__(self, api, info):
        self.api = api
        self.info = info

    def transcribe_file(self, file):
        time.sleep(.1)
        r = sr.Recognizer()
        _, name = os.path.split(file)
        with sr.AudioFile(file) as source:
            audio = r.record(source)
        try:
            if self.api == "Google Speech Recognition":
                transcript = r.recognize_google(audio)
            elif self.api == "Wit.ai":
                key = self.info[0]
                transcript = r.recognize_wit(audio, key=key)
            elif self.api == "Bing":
                key = self.info[0]
                transcript = r.recognize_bing(audio, key=key)
            elif self.api == "Houndify":
                client_id, key = self.info[0], self.info[1]
                transcript = r.recognize_houndify(audio, client_id=client_id, client_key=key)
            else:
                username, password = self.info[0], self.info[1]
                transcript = r.recognize_ibm(audio, username=username, password=password)
            time.sleep(.1)
            return True, name, transcript
        except Exception as e:
            print(e)
            return False, name, ""