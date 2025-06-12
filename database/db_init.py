import sqlite3
from pathlib import Path
import json
from datetime import datetime

def init_database():
    """Initialize the SQLite database with required tables and initial data"""
    db_path = Path("database/news_articles.sqlite")
    
    # Create database directory if it doesn't exist
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create fact checks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim TEXT NOT NULL,
            verdict TEXT NOT NULL,
            confidence REAL NOT NULL,
            source TEXT NOT NULL,
            source_url TEXT NOT NULL,
            explanation TEXT NOT NULL,
            date TEXT NOT NULL,
            related_claims TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    # Create sources table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT,
            api_available BOOLEAN NOT NULL,
            last_updated TEXT NOT NULL
        )
    """)
    
    # Create bias analysis table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bias_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            bias_score REAL NOT NULL,
            bias_category TEXT NOT NULL,
            confidence REAL NOT NULL,
            keywords TEXT,
            created_at TEXT NOT NULL
        )
    """)
    
    # Create media verification table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media_verification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_type TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            is_authentic BOOLEAN NOT NULL,
            confidence REAL NOT NULL,
            manipulation_type TEXT,
            evidence TEXT NOT NULL,
            metadata TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    # Insert initial sources data
    sources = [
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
    
    for source in sources:
        cursor.execute("""
            INSERT OR IGNORE INTO sources (name, url, description, api_available, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (
            source["name"],
            source["url"],
            source["description"],
            source["api_available"],
            datetime.now().isoformat()
        ))
    
    # Create indexes for better query performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_checks_claim ON fact_checks(claim)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_checks_source ON fact_checks(source)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_bias_analysis_text ON bias_analysis(text)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_media_verification_hash ON media_verification(file_hash)")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database() 