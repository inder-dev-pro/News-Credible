from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.image_checker import ImageChecker
from app.services.video_checker import VideoChecker

router = APIRouter()
image_checker = ImageChecker()
video_checker = VideoChecker()

class MediaVerificationResponse(BaseModel):
    is_authentic: bool
    confidence: float
    manipulation_type: str | None
    evidence: List[Dict[str, Any]]
    metadata: Dict[str, Any]

@router.post("/verify_image", response_model=MediaVerificationResponse)
async def verify_image(
    file: UploadFile = File(...),
    perform_reverse_search: bool = True
) -> Dict[str, Any]:
    """
    Analyze an image for signs of manipulation and verify its authenticity.
    
    Args:
        file: The image file to analyze
        perform_reverse_search: Whether to perform reverse image search
        
    Returns:
        MediaVerificationResponse containing analysis results
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Perform image analysis
        result = await image_checker.analyze_image(
            contents,
            perform_reverse_search=perform_reverse_search
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify_video", response_model=MediaVerificationResponse)
async def verify_video(
    file: UploadFile = File(...),
    analyze_frames: bool = True
) -> Dict[str, Any]:
    """
    Analyze a video for signs of manipulation and verify its authenticity.
    
    Args:
        file: The video file to analyze
        analyze_frames: Whether to perform frame-level analysis
        
    Returns:
        MediaVerificationResponse containing analysis results
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Perform video analysis
        result = await video_checker.analyze_video(
            contents,
            analyze_frames=analyze_frames
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supported_formats")
async def get_supported_formats() -> Dict[str, List[str]]:
    """
    Get supported file formats for media verification.
    """
    return {
        "image": ["jpg", "jpeg", "png", "gif", "bmp", "webp"],
        "video": ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
    } 