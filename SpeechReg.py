import speech_recognition as sr


def transcribe_file(file, api, info):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    try:
        if api == "Sphinx":
            transcript =  r.recognize_sphinx(audio)
        elif api == "Google Speech Recognition":
            transcript =  r.recognize_google(audio)
        elif api == "Wit.ai":
            key = info[0]
            transcript = r.recognize_wit(audio, key=key)
        elif api == "Bing":
            key = info[0]
            transcript = r.recognize_bing(audio, key=key)
        elif api == "Houndify":
            clientid, key = info[0], info[1]
            transcript = r.recognize_houndify(audio, client_id=clientid, client_key=key)
        else:
            username, password = info[0], info[1]
            transcript = r.recognize_ibm(audio, username=username, password=password)
        return transcript, True
    except:
        return "error", False




