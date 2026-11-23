def take_command() -> str:
    """Capture voice audio and transcribe to text with safe fallbacks."""
    try:
        import speech_recognition as sr
    except ImportError:
        return "Speech recognition module is not installed."

    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()

    except sr.UnknownValueError:
        return "Sorry, I could not understand."
    except sr.RequestError:
        return "Speech service is unavailable."
    except Exception as e:
        print(f"Voice input notice: {e}")
        return "Microphone is unavailable on this environment."
