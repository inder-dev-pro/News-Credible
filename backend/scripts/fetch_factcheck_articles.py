import asyncio
import aiohttp
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import json
from pathlib import Path
import logging
from typing import Dict, Any, List
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FactCheckFetcher:
    def __init__(self):
        self.db_path = Path("database/news_articles.sqlite")
        self.sources = {
            "politifact": {
                "url": "https://www.politifact.com/factchecks/",
                "parser": self._parse_politifact
            },
            "snopes": {
                "url": "https://www.snopes.com/fact-check/",
                "parser": self._parse_snopes
            },
            "factcheck_org": {
                "url": "https://www.factcheck.org/fake-news/",
                "parser": self._parse_factcheck_org
            },
            "boomlive": {
                "url": "https://www.boomlive.in/fake-news/",
                "parser": self._parse_boomlive
            },
            "altnews": {
                "url": "https://www.altnews.in/topics/fake-news/",
                "parser": self._parse_altnews
            }
        }
    
    async def fetch_all_sources(self):
        """Fetch fact checks from all sources"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for source_name, source_info in self.sources.items():
                tasks.append(self._fetch_source(session, source_name, source_info))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for source_name, result in zip(self.sources.keys(), results):
                if isinstance(result, Exception):
                    logger.error(f"Error fetching {source_name}: {result}")
                else:
                    logger.info(f"Successfully fetched {len(result)} articles from {source_name}")
    
    async def _fetch_source(
        self,
        session: aiohttp.ClientSession,
        source_name: str,
        source_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Fetch fact checks from a specific source"""
        try:
            async with session.get(source_info["url"]) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                
                html = await response.text()
                articles = await source_info["parser"](html)
                
                # Save to database
                self._save_articles(source_name, articles)
                
                return articles
        except Exception as e:
            logger.error(f"Error fetching {source_name}: {e}")
            raise
    
    def _save_articles(self, source: str, articles: List[Dict[str, Any]]):
        """Save articles to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for article in articles:
            cursor.execute("""
                INSERT OR REPLACE INTO fact_checks (
                    claim, verdict, confidence, source, source_url,
                    explanation, date, related_claims, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article["claim"],
                article["verdict"],
                article["confidence"],
                source,
                article["source_url"],
                article["explanation"],
                article["date"],
                json.dumps(article.get("related_claims", [])),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    async def _parse_politifact(self, html: str) -> List[Dict[str, Any]]:
        """Parse PolitiFact articles"""
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # Find all fact-check articles
        for article in soup.find_all("article", class_="m-teaser"):
            try:
                claim = article.find("h3").text.strip()
                verdict = article.find("div", class_="m-teaser__meter").text.strip()
                url = article.find("a")["href"]
                
                articles.append({
                    "claim": claim,
                    "verdict": verdict,
                    "confidence": 0.9,  # Placeholder
                    "source_url": url,
                    "explanation": "",  # Would need to fetch full article
                    "date": datetime.now().isoformat(),  # Would need to parse from article
                    "related_claims": []
                })
            except Exception as e:
                logger.error(f"Error parsing PolitiFact article: {e}")
        
        return articles
    
    async def _parse_snopes(self, html: str) -> List[Dict[str, Any]]:
        """Parse Snopes articles"""
        # TODO: Implement Snopes parsing
        return []
    
    async def _parse_factcheck_org(self, html: str) -> List[Dict[str, Any]]:
        """Parse FactCheck.org articles"""
        # TODO: Implement FactCheck.org parsing
        return []
    
    async def _parse_boomlive(self, html: str) -> List[Dict[str, Any]]:
        """Parse BoomLive articles"""
        # TODO: Implement BoomLive parsing
        return []
    
    async def _parse_altnews(self, html: str) -> List[Dict[str, Any]]:
        """Parse AltNews articles"""
        # TODO: Implement AltNews parsing
        return []

async def main():
    fetcher = FactCheckFetcher()
    await fetcher.fetch_all_sources()

if __name__ == "__main__":
    asyncio.run(main()) 