import speech_recognition as sr
import threading
from app.utils.logger import log_error

_is_listening = False
_stop_event = threading.Event()

WAKE_WORDS = ["friday", "hey friday", "hello friday", "ok friday"]


def detect_wakeword(callback=None, timeout: int = 30) -> str:
    """
    Listen for a wake word. When detected, return or call callback.
    """
    global _is_listening

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            _is_listening = True
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening for wake word...")

            start_time = __import__("time").time()

            while _is_listening:
                if __import__("time").time() - start_time > timeout:
                    _is_listening = False
                    return "Wake word timeout."

                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    text = recognizer.recognize_google(audio).lower().strip()
                    print(f"Heard: {text}")

                    for wake_word in WAKE_WORDS:
                        if wake_word in text:
                            _is_listening = False
                            if callback:
                                callback()
                            return f"Wake word detected: '{text}'"

                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    _is_listening = False
                    return f"Speech service error: {e}"

    except Exception as e:
        log_error("detect_wakeword", e)
        return f"Wake word detection failed: {str(e)}"
    finally:
        _is_listening = False


def stop_listening():
    """Stop the wake word listener."""
    global _is_listening
    _is_listening = False
    return "Wake word listener stopped."


def is_listening() -> bool:
    """Check if the wake word listener is active."""
    return _is_listening
