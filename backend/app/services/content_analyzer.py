from typing import Dict
import requests
from PIL import Image
import numpy as np
import tensorflow_hub as hub
import os
from io import BytesIO
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import aiohttp
import json
import logging
from pathlib import Path
import google.generativeai as genai
from fastapi import HTTPException
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ContentAnalyzer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Gemini
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize models
        self._initialize_models()
        
        # Create cache directory if it doesn't exist
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize cache
        self._initialize_cache()

    def _initialize_models(self):
        """Initialize all required ML models"""
        try:
            # Initialize image analysis model with explicit input size
            self.image_model = hub.load('https://tfhub.dev/google/imagenet/mobilenet_v2_130_224/classification/4')
            self.image_input_size = (224, 224)  # Store expected input size
            
            logger.info("All models initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise

    def _initialize_cache(self):
        """Initialize the cache system"""
        self.cache = {
            'image_analysis': {}
        }
        self.cache_file = self.cache_dir / "analysis_cache.json"
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            except Exception as e:
                logger.error(f"Error loading cache: {str(e)}")

    def _save_cache(self):
        """Save the current cache to disk"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
        except Exception as e:
            logger.error(f"Error saving cache: {str(e)}")

    async def _analyze_image(self, image_url: str, caption: str = None) -> Dict:
        """Analyze image content and verify caption accuracy"""
        try:
            cache_key = f"{image_url}:{caption}" if caption else image_url
            if cache_key in self.cache['image_analysis']:
                return self.cache['image_analysis'][cache_key]

            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image = image.resize((224, 224), Image.Resampling.LANCZOS)
            image_array = np.array(image).astype(np.float32) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            image_embedding = self.image_model(image_array)
            image_embedding_np = image_embedding.numpy()

            # Short, optimized Gemini prompts
            prompt = f"Describe this image. Caption: {caption or 'None'}. Is the caption accurate? Give a confidence score (0-1)."
            response = self.model.generate_content(prompt)
            analysis = response.text

            reverse_search_prompt = f"What is the likely context or event for this image? Any signs of reuse?"
            reverse_search_response = self.model.generate_content(reverse_search_prompt)
            reverse_search_analysis = reverse_search_response.text

            results = {
                'embedding': image_embedding_np.tolist(),
                'caption_verification': analysis,
                'reverse_search': reverse_search_analysis,
                'image_url': image_url,
                'caption': caption
            }
            self.cache['image_analysis'][cache_key] = results
            self._save_cache()
            return results
        except Exception as e:
            logger.error(f"Error in _analyze_image: {str(e)}")
            raise

    async def analyze_url(self, url: str) -> Dict:
        """Analyze content from a URL"""
        try:
            results = {
                'truth_score': 0.0,
                'confidence': 0.0,
                'analysis': {},
                'warnings': []
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=response.status, detail="Failed to fetch URL")
                    html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            images = soup.find_all('img')
            image_results = []
            if images:
                # Limit to 3 images
                limited_images = images[:3]
                tasks = []
                for img in limited_images:
                    img_url = img.get('src')
                    if img_url:
                        caption = img.get('alt', '') or img.get('title', '')
                        if not caption:
                            figcaption = img.find_next('figcaption')
                            if figcaption:
                                caption = figcaption.get_text(strip=True)
                        # Each image analysis has a 100s timeout
                        tasks.append(asyncio.wait_for(self._analyze_image(img_url, caption), timeout=100))
                # Run all image analyses in parallel
                try:
                    image_results = await asyncio.gather(*tasks, return_exceptions=True)
                except Exception as e:
                    logger.warning(f"Image analysis parallelization error: {str(e)}")
                # Filter out failed analyses
                image_results = [res for res in image_results if isinstance(res, dict)]
                if image_results:
                    results['analysis']['images'] = image_results
            if 'images' in results['analysis']:
                results['truth_score'] = self._calculate_truth_score(results['analysis'])
                results['confidence'] = self._calculate_confidence(results['analysis'])
            return results
        except Exception as e:
            logger.error(f"Error in analyze_url: {str(e)}")
            return {"error": str(e), "truth_score": 0.0}

    def _calculate_truth_score(self, analysis: Dict) -> float:
        """Calculate overall truth score based on image analysis"""
        if 'images' not in analysis:
            return 0.0
        
        total_score = 0.0
        total_images = len(analysis['images'])
        
        for img_analysis in analysis['images']:
            # Extract confidence score from Gemini analysis
            try:
                analysis_text = img_analysis['caption_verification']
                # Look for confidence score in the analysis text
                if 'confidence score' in analysis_text.lower():
                    score_text = analysis_text.lower().split('confidence score')[-1]
                    # Extract the first number found
                    import re
                    score_match = re.search(r'\d+\.?\d*', score_text)
                    if score_match:
                        score = float(score_match.group())
                        total_score += score
            except Exception as e:
                logger.warning(f"Error extracting confidence score: {str(e)}")
                continue
        
        return total_score / total_images if total_images > 0 else 0.0

    def _calculate_confidence(self, analysis: Dict) -> float:
        """Calculate confidence score based on analysis quality"""
        if 'images' not in analysis:
            return 0.0
        
        total_confidence = 0.0
        total_images = len(analysis['images'])
        
        for img_analysis in analysis['images']:
            # Check if we have both caption verification and reverse search
            has_caption = bool(img_analysis.get('caption'))
            has_verification = bool(img_analysis.get('caption_verification'))
            has_reverse_search = bool(img_analysis.get('reverse_search'))
            
            # Calculate confidence based on available analysis components
            confidence = 0.0
            if has_caption and has_verification:
                confidence += 0.5
            if has_reverse_search:
                confidence += 0.5
            
            total_confidence += confidence
        
        return total_confidence / total_images if total_images > 0 else 0.0