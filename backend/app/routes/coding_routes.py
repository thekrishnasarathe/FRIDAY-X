from fastapi import APIRouter
from pydantic import BaseModel
from app.modules.coding.code_helper import explain_code, run_python_code, get_code_suggestion
from app.modules.coding.debug_helper import analyze_error, check_syntax
from app.modules.coding.project_builder import create_project

router = APIRouter()


class CodeRequest(BaseModel):
    code: str
    language: str = "python"


class PromptRequest(BaseModel):
    prompt: str


class ProjectRequest(BaseModel):
    name: str
    project_type: str = "python"  # python, web, basic


class ErrorRequest(BaseModel):
    error: str
    language: str = "python"


@router.post("/explain")
def explain_code_route(request: CodeRequest):
    result = explain_code(request.language, request.code)
    return {"result": result}


@router.post("/run")
def run_code_route(request: CodeRequest):
    if request.language != "python":
        return {"result": "Only Python execution is supported."}
    result = run_python_code(request.code)
    return {"result": result}


@router.post("/suggest")
def suggest_code_route(request: PromptRequest):
    result = get_code_suggestion(request.prompt)
    return {"result": result}


@router.post("/debug")
def debug_error_route(request: ErrorRequest):
    result = analyze_error(request.error, request.language)
    return {"result": result}


@router.post("/syntax-check")
def syntax_check_route(request: CodeRequest):
    result = check_syntax(request.code, request.language)
    return {"result": result}


@router.post("/create-project")
def create_project_route(request: ProjectRequest):
    result = create_project(request.name, request.project_type)
    return {"result": result}
