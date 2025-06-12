from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any

app = FastAPI(
    title="NewsCredible API",
    description="API for detecting media bias and verifying content authenticity",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint returning API status"""
    return {
        "status": "online",
        "service": "NewsCredible API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}

# Import and include routers
from app.routers import text_bias, media_verify, search_factcheck

app.include_router(text_bias.router, prefix="/api/v1", tags=["Text Analysis"])
app.include_router(media_verify.router, prefix="/api/v1", tags=["Media Verification"])
app.include_router(search_factcheck.router, prefix="/api/v1", tags=["Fact Checking"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 