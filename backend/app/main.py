from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from app.routers import content, media_verify, search_factcheck

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="NewsCredible API",
    description="API for analyzing content truthfulness using Gemini AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","https://www.newscredible.tech", "http://localhost:8000","https://news-credible-backend.onrender.com"],  # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"status": "online", "message": "NewsCredible API is running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(content.router, prefix="/api/v1", tags=["content"])
app.include_router(media_verify.router, prefix="/api/v1", tags=["media"])
app.include_router(search_factcheck.router, prefix="/api/v1", tags=["fact-check"])

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Use PORT env variable if set, else default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port) 