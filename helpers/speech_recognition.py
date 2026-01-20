import speech_recognition as sr

def speech_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
        try:
            return r.recognize_google(audio)
        except:
            return "Could not detect speech"
