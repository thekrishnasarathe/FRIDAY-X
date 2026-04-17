from fastapi import APIRouter
from pydantic import BaseModel
from app.modules.security.auth_manager import (
    lock_assistant, unlock_assistant, set_passphrase, get_security_status
)
from app.modules.security.session_guard import (
    start_session, end_session, get_session_info
)

router = APIRouter()


class PassphraseRequest(BaseModel):
    passphrase: str


@router.post("/lock")
def lock_route():
    result = lock_assistant()
    return {"result": result}


@router.post("/unlock")
def unlock_route(request: PassphraseRequest):
    result = unlock_assistant(request.passphrase)
    return {"result": result}


@router.post("/set-passphrase")
def set_passphrase_route(request: PassphraseRequest):
    result = set_passphrase(request.passphrase)
    return {"result": result}


@router.get("/status")
def security_status_route():
    result = get_security_status()
    return {"result": result}


@router.post("/start-session")
def start_session_route():
    result = start_session()
    return {"result": result}


@router.post("/end-session")
def end_session_route():
    result = end_session()
    return {"result": result}


@router.get("/session-info")
def session_info_route():
    result = get_session_info()
    return {"result": result}
