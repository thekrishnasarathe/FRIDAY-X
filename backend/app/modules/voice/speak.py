import os
import threading

_speak_lock = threading.Lock()


def speak_text(text: str) -> None:
    """Safely convert text to speech with cross-platform fallback."""
    if not text:
        return

    try:
        with _speak_lock:
            try:
                import pyttsx3
            except ImportError:
                print(f"TTS offline (pyttsx3 not installed): {text}")
                return

            driver = 'sapi5' if os.name == 'nt' else None
            try:
                engine = pyttsx3.init(driverName=driver) if driver else pyttsx3.init()
            except Exception:
                try:
                    engine = pyttsx3.init()
                except Exception as init_err:
                    print(f"TTS driver init error: {init_err}")
                    return

            engine.setProperty("rate", 170)
            engine.setProperty("volume", 1.0)

            try:
                voices = engine.getProperty("voices")
                if voices:
                    engine.setProperty("voice", voices[0].id)
            except Exception:
                pass

            print(f"FRIDAY says: {text}")
            engine.say(text)
            engine.runAndWait()
            engine.stop()

    except Exception as e:
        print(f"TTS Warning: {e}")
