from fastapi import APIRouter
from pydantic import BaseModel
from app.modules.automation.file_control import create_folder, create_file
from app.modules.files.file_searcher import search_files, get_recent_files
from app.modules.files.note_parser import read_file, get_file_info

router = APIRouter()


class FileCreateRequest(BaseModel):
    name: str


class SearchRequest(BaseModel):
    query: str
    file_type: str = None


class FilePathRequest(BaseModel):
    path: str


@router.post("/create-folder")
def create_folder_route(request: FileCreateRequest):
    result = create_folder(request.name)
    return {"result": result}


@router.post("/create-file")
def create_file_route(request: FileCreateRequest):
    result = create_file(request.name)
    return {"result": result}


@router.post("/search")
def search_files_route(request: SearchRequest):
    result = search_files(request.query, request.file_type)
    return {"result": result}


@router.get("/recent")
def recent_files_route(folder: str = "Desktop", count: int = 10):
    result = get_recent_files(folder, count)
    return {"result": result}


@router.post("/read")
def read_file_route(request: FilePathRequest):
    result = read_file(request.path)
    return {"result": result}


@router.post("/info")
def file_info_route(request: FilePathRequest):
    result = get_file_info(request.path)
    return {"result": result}
