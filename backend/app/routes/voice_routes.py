from fastapi import APIRouter
from app.modules.voice.listen import take_command
from app.modules.voice.speak import speak_text
from app.core.brain import process_command

router = APIRouter()

@router.get("/listen")
def listen_voice():
    command = take_command()

    if not command:
        response = "I did not hear anything."
        speak_text(response)
        return {"command": "", "response": response}

    response = process_command(command)

    if not response:
        response = "Command executed."

    speak_text(response)

    return {
        "command": command,
        "response": response
    }