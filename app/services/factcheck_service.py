import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
import sqlite3
from datetime import datetime
import json
from pathlib import Path
import os
from bs4 import BeautifulSoup
import re

class FactCheckService:
    def __init__(self):
        self.db_path = Path("database/news_articles.sqlite")
        self._init_database()
        
    def _init_database(self):
        """Initialize the SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
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
        
        conn.commit()
        conn.close()
    
    async def search_claims(
        self,
        text: str,
        source_url: Optional[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for fact checks related to the given text.
        
        Args:
            text: The text to search for
            source_url: Optional URL to filter results by source
            max_results: Maximum number of results to return
            
        Returns:
            List of fact check results
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Prepare search query
        query = """
            SELECT * FROM fact_checks
            WHERE claim LIKE ?
            OR explanation LIKE ?
        """
        params = [f"%{text}%", f"%{text}%"]
        
        if source_url:
            query += " AND source_url = ?"
            params.append(source_url)
        
        query += " ORDER BY confidence DESC LIMIT ?"
        params.append(max_results)
        
        # Execute query
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Convert results to dictionaries
        fact_checks = []
        for row in results:
            fact_checks.append({
                "claim": row[1],
                "verdict": row[2],
                "confidence": row[3],
                "source": row[4],
                "source_url": row[5],
                "explanation": row[6],
                "date": row[7],
                "related_claims": json.loads(row[8]) if row[8] else []
            })
        
        conn.close()
        return fact_checks
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the fact-checking database.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total number of fact checks
        cursor.execute("SELECT COUNT(*) FROM fact_checks")
        total_checks = cursor.fetchone()[0]
        
        # Get number of fact checks by source
        cursor.execute("""
            SELECT source, COUNT(*) as count
            FROM fact_checks
            GROUP BY source
        """)
        checks_by_source = dict(cursor.fetchall())
        
        # Get number of fact checks by verdict
        cursor.execute("""
            SELECT verdict, COUNT(*) as count
            FROM fact_checks
            GROUP BY verdict
        """)
        checks_by_verdict = dict(cursor.fetchall())
        
        # Get average confidence by source
        cursor.execute("""
            SELECT source, AVG(confidence) as avg_confidence
            FROM fact_checks
            GROUP BY source
        """)
        confidence_by_source = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            "total_fact_checks": total_checks,
            "checks_by_source": checks_by_source,
            "checks_by_verdict": checks_by_verdict,
            "confidence_by_source": confidence_by_source,
            "last_updated": datetime.now().isoformat()
        }
    
    async def update_fact_checks(self):
        """
        Update the fact-checking database by scraping supported sources.
        """
        # TODO: Implement web scraping for each source
        # This is a placeholder implementation
        pass
    
    async def _scrape_politifact(self) -> List[Dict[str, Any]]:
        """
        Scrape fact checks from PolitiFact.
        """
        # TODO: Implement PolitiFact scraping
        return []
    
    async def _scrape_snopes(self) -> List[Dict[str, Any]]:
        """
        Scrape fact checks from Snopes.
        """
        # TODO: Implement Snopes scraping
        return []
    
    async def _scrape_factcheck_org(self) -> List[Dict[str, Any]]:
        """
        Scrape fact checks from FactCheck.org.
        """
        # TODO: Implement FactCheck.org scraping
        return []
    
    async def _scrape_boomlive(self) -> List[Dict[str, Any]]:
        """
        Scrape fact checks from BoomLive.
        """
        # TODO: Implement BoomLive scraping
        return []
    
    async def _scrape_altnews(self) -> List[Dict[str, Any]]:
        """
        Scrape fact checks from AltNews.
        """
        # TODO: Implement AltNews scraping
        return [] 