from typing import Dict, List, Optional, Union
import requests
from PIL import Image
import imagehash
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import os
from io import BytesIO
from dotenv import load_dotenv
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import openai
from openai import OpenAI
import cv2
import aiohttp
import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
import google.generativeai as genai

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
            # Check cache first
            cache_key = f"{image_url}:{caption}" if caption else image_url
            if cache_key in self.cache['image_analysis']:
                return self.cache['image_analysis'][cache_key]
            
            # Download and process image
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image to match model's expected input size
            image = image.resize((224, 224), Image.Resampling.LANCZOS)
            
            # Convert to numpy array and normalize
            image_array = np.array(image)
            image_array = image_array.astype(np.float32) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            
            # Get image embeddings and convert to numpy array
            image_embedding = self.image_model(image_array)
            image_embedding_np = image_embedding.numpy()
            
            # Use Gemini for image analysis and caption verification
            prompt = f"""Analyze this image and verify if the caption accurately describes it:

Image URL: {image_url}
Caption: {caption if caption else 'No caption provided'}

Please provide:
1. A detailed description of what is actually shown in the image
2. Whether the caption accurately describes the image content
3. Any potential misrepresentations or misleading elements
4. The likely context or event shown in the image
5. A confidence score (0-1) for your analysis"""
            
            response = self.model.generate_content(prompt)
            analysis = response.text
            
            # Perform reverse image search using Gemini
            reverse_search_prompt = f"""Based on the image content, identify:
1. The likely original event or context
2. When this image might have been taken
3. Any notable landmarks, people, or objects that could help identify the original source
4. Whether this image appears to be from its original context or if it might be reused/misused

Image URL: {image_url}"""
            
            reverse_search_response = self.model.generate_content(reverse_search_prompt)
            reverse_search_analysis = reverse_search_response.text
            
            results = {
                'embedding': image_embedding_np.tolist(),
                'caption_verification': analysis,
                'reverse_search': reverse_search_analysis,
                'image_url': image_url,
                'caption': caption
            }
            
            # Cache results
            self.cache['image_analysis'][cache_key] = results
            self._save_cache()
            
            return results
            
        except Exception as e:
            logger.error(f"Error in _analyze_image: {str(e)}")
            raise

    async def analyze_url(self, url: str) -> Dict:
        """Analyze content from a URL"""
        try:
            # Initialize results
            results = {
                'truth_score': 0.0,
                'confidence': 0.0,
                'analysis': {},
                'warnings': []
            }
            
            # Fetch content from URL
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=response.status, detail="Failed to fetch URL")
                    html = await response.text()
            
            # Parse HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract images with their captions
            images = soup.find_all('img')
            if images:
                image_results = []
                for img in images:
                    img_url = img.get('src')
                    if img_url:
                        # Get caption from alt text, title, or nearby figcaption
                        caption = img.get('alt', '')
                        if not caption:
                            caption = img.get('title', '')
                        if not caption:
                            figcaption = img.find_next('figcaption')
                            if figcaption:
                                caption = figcaption.get_text(strip=True)
                        
                        try:
                            img_analysis = await self._analyze_image(img_url, caption)
                            image_results.append(img_analysis)
                        except Exception as e:
                            logger.warning(f"Failed to analyze image {img_url}: {str(e)}")
                
                if image_results:
                    results['analysis']['images'] = image_results
            
            # Calculate overall truth score based on image analysis
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