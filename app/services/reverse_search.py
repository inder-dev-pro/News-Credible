import aiohttp
import base64
from typing import Dict, Any, List
import io
from PIL import Image
import hashlib
import os
from pathlib import Path

class ReverseImageSearch:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_VISION_API_KEY", "")
        self.search_engines = ["google", "bing"]
        
    async def search(self, image_data: bytes) -> List[Dict[str, Any]]:
        """
        Perform reverse image search using multiple search engines.
        
        Args:
            image_data: Raw image data in bytes
            
        Returns:
            List of search results from different engines
        """
        results = []
        
        # Perform search with each engine
        for engine in self.search_engines:
            try:
                if engine == "google":
                    engine_results = await self._search_google(image_data)
                elif engine == "bing":
                    engine_results = await self._search_bing(image_data)
                else:
                    continue
                
                results.append({
                    "engine": engine,
                    "results": engine_results
                })
            except Exception as e:
                print(f"Error searching with {engine}: {e}")
                results.append({
                    "engine": engine,
                    "error": str(e)
                })
        
        return results
    
    async def _search_google(self, image_data: bytes) -> List[Dict[str, Any]]:
        """
        Search for similar images using Google Vision API.
        """
        if not self.api_key:
            return [{
                "error": "Google Vision API key not configured"
            }]
        
        # Encode image data
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        
        # Prepare API request
        url = f"https://vision.googleapis.com/v1/images:annotate?key={self.api_key}"
        payload = {
            "requests": [{
                "image": {
                    "content": encoded_image
                },
                "features": [{
                    "type": "WEB_DETECTION",
                    "maxResults": 10
                }]
            }]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    return [{
                        "error": f"API request failed with status {response.status}"
                    }]
                
                data = await response.json()
                
                # Extract web detection results
                web_detection = data.get("responses", [{}])[0].get("webDetection", {})
                
                return [{
                    "url": match.get("url", ""),
                    "title": match.get("title", ""),
                    "score": match.get("score", 0.0)
                } for match in web_detection.get("webEntities", [])]
    
    async def _search_bing(self, image_data: bytes) -> List[Dict[str, Any]]:
        """
        Search for similar images using Bing Visual Search API.
        """
        # TODO: Implement Bing Visual Search
        # This is a placeholder implementation
        return [{
            "error": "Bing Visual Search not implemented"
        }]
    
    def _compute_image_hash(self, image_data: bytes) -> str:
        """
        Compute perceptual hash of the image for deduplication.
        """
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Resize to 8x8 and convert to grayscale
        image = image.resize((8, 8), Image.Resampling.LANCZOS).convert('L')
        
        # Compute average pixel value
        pixels = list(image.getdata())
        avg = sum(pixels) / len(pixels)
        
        # Create hash
        bits = ''.join('1' if pixel > avg else '0' for pixel in pixels)
        return hashlib.md5(bits.encode()).hexdigest() 