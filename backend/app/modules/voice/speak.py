import pyttsx3
import threading

_speak_lock = threading.Lock()

def speak_text(text):
    try:
        with _speak_lock:
            engine = pyttsx3.init(driverName='sapi5')
            engine.setProperty("rate", 170)
            engine.setProperty("volume", 1.0)

            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)

            print(f"FRIDAY says: {text}")
            engine.say(text)
            engine.runAndWait()
            engine.stop()

    except Exception as e:
        print(f"TTS Error: {e}")