from fastapi import APIRouter
from pydantic import BaseModel
from app.modules.communication.email_sender import send_email
from app.modules.communication.whatsapp_sender import send_whatsapp

router = APIRouter()


class EmailRequest(BaseModel):
    to: str
    subject: str = "Message from FRIDAY"
    body: str


class WhatsAppRequest(BaseModel):
    phone: str  # with country code e.g. +919876543210
    message: str


@router.post("/email")
def send_email_route(request: EmailRequest):
    result = send_email(request.to, request.subject, request.body)
    return {"result": result}


@router.post("/whatsapp")
def send_whatsapp_route(request: WhatsAppRequest):
    result = send_whatsapp(request.phone, request.message)
    return {"result": result}
