from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from app.services.factcheck_service import FactCheckService

router = APIRouter()
factcheck_service = FactCheckService()

class FactCheckQuery(BaseModel):
    text: str
    source_url: Optional[str] = None
    max_results: int = 5

class FactCheckResult(BaseModel):
    claim: str
    verdict: str
    confidence: float
    source: str
    source_url: str
    explanation: str
    date: str
    related_claims: List[str]

@router.post("/search_factcheck", response_model=List[FactCheckResult])
async def search_factcheck(query: FactCheckQuery) -> List[Dict[str, Any]]:
    """
    Search fact-checking databases for claims similar to the input text.
    
    Args:
        query: FactCheckQuery object containing the text to search for
        
    Returns:
        List of FactCheckResult objects containing matching fact checks
    """
    try:
        results = await factcheck_service.search_claims(
            query.text,
            source_url=query.source_url,
            max_results=query.max_results
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/factcheck_sources")
async def get_factcheck_sources() -> Dict[str, List[Dict[str, str]]]:
    """
    Get list of supported fact-checking sources and their details.
    """
    return {
        "sources": [
            {
                "name": "PolitiFact",
                "url": "https://www.politifact.com",
                "description": "Fact-checking website that rates the accuracy of claims by elected officials and others",
                "api_available": True
            },
            {
                "name": "Snopes",
                "url": "https://www.snopes.com",
                "description": "Fact-checking website that researches urban legends, myths, rumors, and misinformation",
                "api_available": False
            },
            {
                "name": "FactCheck.org",
                "url": "https://www.factcheck.org",
                "description": "Non-partisan fact-checking website that monitors the factual accuracy of political statements",
                "api_available": False
            },
            {
                "name": "BoomLive",
                "url": "https://www.boomlive.in",
                "description": "Indian fact-checking website focusing on viral content and misinformation",
                "api_available": False
            },
            {
                "name": "AltNews",
                "url": "https://www.altnews.in",
                "description": "Indian fact-checking website focusing on misinformation and fake news",
                "api_available": False
            }
        ]
    }

@router.get("/factcheck_stats")
async def get_factcheck_stats() -> Dict[str, Any]:
    """
    Get statistics about the fact-checking database.
    """
    try:
        stats = await factcheck_service.get_database_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 