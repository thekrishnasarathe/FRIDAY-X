import speech_recognition as sr

def take_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()

    except sr.UnknownValueError:
        return "Sorry, I could not understand."

    except sr.RequestError:
        return "Speech service is unavailable."