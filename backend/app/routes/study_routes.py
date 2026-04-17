from fastapi import APIRouter
from pydantic import BaseModel
from app.modules.study.notes_helper import create_note, list_notes, summarize_topic
from app.modules.study.quiz_generator import generate_quiz, generate_flashcards
from app.modules.study.revision_planner import create_revision_plan, suggest_resources

router = APIRouter()


class NoteRequest(BaseModel):
    title: str
    content: str = ""


class TopicRequest(BaseModel):
    topic: str
    count: int = 5


class RevisionRequest(BaseModel):
    subject: str
    days: int = 7


@router.post("/create-note")
def create_note_route(request: NoteRequest):
    result = create_note(request.title, request.content)
    return {"result": result}


@router.get("/list-notes")
def list_notes_route():
    result = list_notes()
    return {"result": result}


@router.post("/summarize")
def summarize_route(request: TopicRequest):
    result = summarize_topic(request.topic)
    return {"result": result}


@router.post("/quiz")
def quiz_route(request: TopicRequest):
    result = generate_quiz(request.topic, request.count)
    return {"result": result}


@router.post("/flashcards")
def flashcards_route(request: TopicRequest):
    result = generate_flashcards(request.topic, request.count)
    return {"result": result}


@router.post("/revision-plan")
def revision_plan_route(request: RevisionRequest):
    result = create_revision_plan(request.subject, request.days)
    return {"result": result}


@router.post("/resources")
def resources_route(request: TopicRequest):
    result = suggest_resources(request.topic)
    return {"result": result}
