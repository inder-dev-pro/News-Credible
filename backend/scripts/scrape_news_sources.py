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
from newspaper import Article
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        self.db_path = Path("database/news_articles.sqlite")
        self.sources = {
            "reuters": {
                "url": "https://www.reuters.com",
                "categories": ["world", "business", "technology"]
            },
            "ap": {
                "url": "https://www.apnews.com",
                "categories": ["world", "politics", "business"]
            },
            "bbc": {
                "url": "https://www.bbc.com/news",
                "categories": ["world", "business", "technology"]
            },
            "cnn": {
                "url": "https://www.cnn.com",
                "categories": ["world", "politics", "business"]
            },
            "fox": {
                "url": "https://www.foxnews.com",
                "categories": ["world", "politics", "business"]
            }
        }
    
    async def scrape_all_sources(self):
        """Scrape articles from all sources"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for source_name, source_info in self.sources.items():
                for category in source_info["categories"]:
                    tasks.append(
                        self._scrape_source_category(
                            session,
                            source_name,
                            source_info["url"],
                            category
                        )
                    )
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Error scraping: {result}")
                else:
                    logger.info(f"Successfully scraped {len(result)} articles")
    
    async def _scrape_source_category(
        self,
        session: aiohttp.ClientSession,
        source: str,
        base_url: str,
        category: str
    ) -> List[Dict[str, Any]]:
        """Scrape articles from a specific source and category"""
        try:
            # Construct category URL
            category_url = f"{base_url}/{category}"
            
            async with session.get(category_url) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                
                html = await response.text()
                article_urls = self._extract_article_urls(html, base_url)
                
                # Fetch and parse articles
                articles = []
                for url in article_urls[:10]:  # Limit to 10 articles per category
                    try:
                        article = await self._fetch_article(session, url)
                        if article:
                            article["source"] = source
                            article["category"] = category
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Error fetching article {url}: {e}")
                
                # Save to database
                self._save_articles(articles)
                
                return articles
        except Exception as e:
            logger.error(f"Error scraping {source}/{category}: {e}")
            raise
    
    def _extract_article_urls(self, html: str, base_url: str) -> List[str]:
        """Extract article URLs from the page"""
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        
        # Find all article links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/"):
                href = base_url + href
            if self._is_article_url(href):
                urls.append(href)
        
        return list(set(urls))  # Remove duplicates
    
    def _is_article_url(self, url: str) -> bool:
        """Check if URL is likely an article"""
        article_patterns = [
            r"/article/",
            r"/story/",
            r"/news/",
            r"/world/",
            r"/business/",
            r"/technology/",
            r"/politics/"
        ]
        return any(re.search(pattern, url) for pattern in article_patterns)
    
    async def _fetch_article(
        self,
        session: aiohttp.ClientSession,
        url: str
    ) -> Dict[str, Any]:
        """Fetch and parse an article"""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                
                html = await response.text()
                
                # Use newspaper3k to parse article
                article = Article(url)
                article.set_html(html)
                article.parse()
                
                # Generate article hash
                content_hash = hashlib.md5(
                    (article.title + article.text).encode()
                ).hexdigest()
                
                return {
                    "url": url,
                    "title": article.title,
                    "text": article.text,
                    "authors": article.authors,
                    "publish_date": article.publish_date.isoformat() if article.publish_date else None,
                    "content_hash": content_hash,
                    "created_at": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error parsing article {url}: {e}")
            return None
    
    def _save_articles(self, articles: List[Dict[str, Any]]):
        """Save articles to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for article in articles:
            cursor.execute("""
                INSERT OR REPLACE INTO news_articles (
                    url, title, text, authors, publish_date,
                    content_hash, source, category, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article["url"],
                article["title"],
                article["text"],
                json.dumps(article["authors"]),
                article["publish_date"],
                article["content_hash"],
                article["source"],
                article["category"],
                article["created_at"]
            ))
        
        conn.commit()
        conn.close()

async def main():
    scraper = NewsScraper()
    await scraper.scrape_all_sources()

if __name__ == "__main__":
    asyncio.run(main()) 