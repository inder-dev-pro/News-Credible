from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.bias_detector import BiasDetector

router = APIRouter()
bias_detector = BiasDetector()

class TextInput(BaseModel):
    text: str
    source_url: str | None = None

class BiasResponse(BaseModel):
    bias_score: float
    bias_category: str
    confidence: float
    explanation: str
    keywords: List[str]

@router.post("/detect_bias", response_model=BiasResponse)
async def detect_bias(input_data: TextInput) -> Dict[str, Any]:
    """
    Analyze text for political bias and sensationalism.
    
    Args:
        input_data: TextInput object containing the text to analyze
        
    Returns:
        BiasResponse object containing bias analysis results
    """
    try:
        result = await bias_detector.analyze_text(input_data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch_detect_bias")
async def batch_detect_bias(texts: List[TextInput]) -> List[BiasResponse]:
    """
    Analyze multiple texts for bias in batch.
    
    Args:
        texts: List of TextInput objects
        
    Returns:
        List of BiasResponse objects
    """
    try:
        results = await bias_detector.analyze_batch([t.text for t in texts])
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bias_categories")
async def get_bias_categories() -> Dict[str, str]:
    """
    Get available bias categories and their descriptions.
    """
    return {
        "left": "Left-leaning content with progressive/liberal bias",
        "right": "Right-leaning content with conservative bias",
        "center": "Balanced content with minimal bias",
        "sensationalist": "Content using exaggerated or emotional language",
        "neutral": "Objective content with minimal bias"
    } 