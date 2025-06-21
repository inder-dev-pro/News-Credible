from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Optional
from ..services.content_analyzer import ContentAnalyzer
from pydantic import BaseModel, HttpUrl

router = APIRouter()

def get_content_analyzer():
    if not hasattr(get_content_analyzer, "instance"):
        get_content_analyzer.instance = ContentAnalyzer()
    return get_content_analyzer.instance

class URLRequest(BaseModel):
    url: HttpUrl

@router.post("/analyze/url")
async def analyze_url(request: URLRequest) -> Dict:
    """Analyze content from a URL."""
    try:
        analyzer = get_content_analyzer()
        result = await analyzer.analyze_url(str(request.url))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)) -> Dict:
    """Analyze an uploaded image."""
    try:
        analyzer = get_content_analyzer()
        contents = await file.read()
        result = await analyzer.analyze_image(contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/video")
async def analyze_video(file: UploadFile = File(...)) -> Dict:
    """Analyze an uploaded video."""
    try:
        analyzer = get_content_analyzer()
        contents = await file.read()
        result = await analyzer.analyze_video(contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 