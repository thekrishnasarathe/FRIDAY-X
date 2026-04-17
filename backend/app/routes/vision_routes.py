from fastapi import APIRouter
from pydantic import BaseModel
from app.modules.vision.screenshot_reader import take_screenshot, read_screenshot_text
from app.modules.vision.image_analyzer import analyze_image, describe_screenshot

router = APIRouter()


class ImageRequest(BaseModel):
    image_path: str


@router.get("/screenshot")
def screenshot_route():
    result = take_screenshot()
    return {"result": result}


@router.get("/read-screen")
def read_screen_route():
    result = read_screenshot_text()
    return {"result": result}


@router.post("/analyze")
def analyze_image_route(request: ImageRequest):
    result = analyze_image(request.image_path)
    return {"result": result}


@router.get("/describe-screen")
def describe_screen_route():
    result = describe_screenshot()
    return {"result": result}
