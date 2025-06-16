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
            # Initialize sentence transformer for text analysis
            self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize image analysis model with explicit input size
            self.image_model = hub.load('https://tfhub.dev/google/imagenet/mobilenet_v2_130_224/classification/4')
            self.image_input_size = (224, 224)  # Store expected input size
            
            # Initialize fact-checking model
            self.fact_checker = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")
            
            logger.info("All models initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise

    def _initialize_cache(self):
        """Initialize the cache system"""
        self.cache = {
            'text_analysis': {},
            'image_analysis': {},
            'fact_checking': {},
            'video_analysis': {},
            'source_analysis': {}
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
            
            # Extract text content
            text_content = soup.get_text(separator=' ', strip=True)
            if text_content:
                text_results = await self._analyze_text(text_content)
                results['analysis']['text'] = text_results
            
            # Extract images
            images = soup.find_all('img')
            if images:
                image_results = []
                for img in images:
                    img_url = img.get('src')
                    if img_url:
                        try:
                            img_analysis = await self._analyze_image(img_url)
                            image_results.append(img_analysis)
                        except Exception as e:
                            logger.warning(f"Failed to analyze image {img_url}: {str(e)}")
                if image_results:
                    results['analysis']['images'] = image_results
            
            # Extract videos
            videos = soup.find_all(['video', 'iframe'])
            if videos:
                video_results = []
                for video in videos:
                    video_url = video.get('src')
                    if video_url:
                        try:
                            video_analysis = await self._analyze_video(video_url)
                            video_results.append(video_analysis)
                        except Exception as e:
                            logger.warning(f"Failed to analyze video {video_url}: {str(e)}")
                if video_results:
                    results['analysis']['videos'] = video_results
            
            # Analyze source
            source_results = await self._analyze_source(url)
            results['analysis']['source'] = source_results
            
            # Calculate overall truth score
            results['truth_score'] = self._calculate_truth_score(results['analysis'])
            
            # Calculate confidence
            results['confidence'] = self._calculate_confidence(results['analysis'])
            
            return results
            
        except Exception as e:
            logger.error(f"Error in analyze_url: {str(e)}")
            return {"error": str(e), "truth_score": 0.0}

    async def _analyze_text(self, text: str) -> Dict:
        """Analyze text content for truthfulness"""
        try:
            # Check cache first
            cache_key = text[:100]  # Use first 100 chars as key
            if cache_key in self.cache['text_analysis']:
                return self.cache['text_analysis'][cache_key]
            
            # Split text into chunks of approximately 400 tokens (leaving room for prompt)
            chunks = self._split_text_into_chunks(text, max_tokens=400)
            
            # Process each chunk
            chunk_results = []
            for chunk in chunks:
                # Get text embeddings for chunk
                chunk_embedding = self.text_model.encode(chunk)
                
                # Perform fact-checking on chunk
                fact_check_result = self.fact_checker(chunk)[0]
                
                # Use Gemini for additional analysis
                response = self.model.generate_content(
                    f"""You are a fact-checking assistant. Analyze the following text for potential misinformation, bias, or factual inaccuracies:

Text: {chunk}

Provide a detailed analysis focusing on:
1. Potential misinformation
2. Bias detection
3. Factual accuracy
4. Overall credibility assessment"""
                )
                
                chunk_results.append({
                    'embedding': chunk_embedding.tolist(),
                    'fact_check_score': fact_check_result['score'],
                    'fact_check_label': fact_check_result['label'],
                    'gemini_analysis': response.text
                })
            
            # Combine results
            results = {
                'chunks': chunk_results,
                'fact_check_score': sum(r['fact_check_score'] for r in chunk_results) / len(chunk_results),
                'fact_check_label': max((r['fact_check_label'] for r in chunk_results), key=lambda x: x['score']),
                'gemini_analysis': '\n\n'.join(r['gemini_analysis'] for r in chunk_results)
            }
            
            # Cache results
            self.cache['text_analysis'][cache_key] = results
            self._save_cache()
            
            return results
            
        except Exception as e:
            logger.error(f"Error in _analyze_text: {str(e)}")
            raise

    def _split_text_into_chunks(self, text: str, max_tokens: int = 400) -> List[str]:
        """Split text into chunks of approximately max_tokens length"""
        # Simple splitting by sentences first
        sentences = text.split('. ')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            # Rough estimate of tokens (words + punctuation)
            sentence_length = len(sentence.split())
            
            if current_length + sentence_length > max_tokens:
                if current_chunk:
                    chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        
        return chunks

    async def _analyze_image(self, image_url: str) -> Dict:
        """Analyze image content for truthfulness"""
        try:
            # Check cache first
            if image_url in self.cache['image_analysis']:
                return self.cache['image_analysis'][image_url]
            
            # Download and process image
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image to match model's expected input size (224x224)
            image = image.resize((224, 224), Image.Resampling.LANCZOS)
            
            # Convert to numpy array and normalize
            image_array = np.array(image)
            image_array = image_array.astype(np.float32) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            # Get image embeddings
            image_embedding = self.image_model(image_array)
            
            # Use Gemini for image analysis
            response = self.model.generate_content(
                f"""Analyze this image for potential manipulation, misleading content, or suspicious elements:
Image URL: {image_url}

Provide a detailed analysis focusing on:
1. Image authenticity
2. Potential manipulation
3. Context and representation
4. Overall credibility assessment"""
            )
            
            analysis = response.text
            
            results = {
                'embedding': image_embedding.numpy().tolist(),
                'gemini_analysis': analysis
            }
            
            # Cache results
            self.cache['image_analysis'][image_url] = results
            self._save_cache()
            
            return results
            
        except Exception as e:
            logger.error(f"Error in _analyze_image: {str(e)}")
            raise

    async def _analyze_video(self, video_url: str) -> Dict:
        """Analyze video content for truthfulness"""
        try:
            # Check cache first
            if video_url in self.cache['video_analysis']:
                return self.cache['video_analysis'][video_url]
            
            # Extract frames from video
            frames = self._extract_video_frames(video_url)
            
            # Analyze each frame
            frame_analyses = []
            for frame in frames:
                frame_analysis = await self._analyze_image(frame)
                frame_analyses.append(frame_analysis)
            
            # Use Gemini for video analysis
            response = self.model.generate_content(
                f"""Analyze this video for potential manipulation, misleading content, or suspicious elements:
Video URL: {video_url}

Provide a detailed analysis focusing on:
1. Video authenticity
2. Potential manipulation
3. Context and representation
4. Overall credibility assessment"""
            )
            
            analysis = response.text
            
            results = {
                'frame_analyses': frame_analyses,
                'gemini_analysis': analysis
            }
            
            # Cache results
            self.cache['video_analysis'][video_url] = results
            self._save_cache()
            
            return results
            
        except Exception as e:
            logger.error(f"Error in _analyze_video: {str(e)}")
            raise

    async def _analyze_source(self, source_url: str) -> Dict:
        """Analyze the source of the content"""
        try:
            # Check cache first
            if source_url in self.cache['source_analysis']:
                return self.cache['source_analysis'][source_url]
            
            async with aiohttp.ClientSession() as session:
                async with session.get(source_url) as response:
                    html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract metadata
            metadata = {
                'title': soup.title.string if soup.title else None,
                'description': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else None,
                'author': soup.find('meta', {'name': 'author'})['content'] if soup.find('meta', {'name': 'author'}) else None,
                'publish_date': soup.find('meta', {'property': 'article:published_time'})['content'] if soup.find('meta', {'property': 'article:published_time'}) else None
            }
            
            # Use Gemini for source analysis
            response = self.model.generate_content(
                f"""Analyze this source for reliability and trustworthiness:
Source URL: {source_url}
Metadata: {json.dumps(metadata, indent=2)}

Provide a detailed analysis focusing on:
1. Source credibility
2. Content quality
3. Potential biases
4. Overall trustworthiness assessment"""
            )
            
            analysis = response.text
            
            results = {
                'metadata': metadata,
                'gemini_analysis': analysis
            }
            
            # Cache results
            self.cache['source_analysis'][source_url] = results
            self._save_cache()
            
            return results
            
        except Exception as e:
            logger.error(f"Error in _analyze_source: {str(e)}")
            raise

    def _calculate_truth_score(self, analysis: Dict) -> float:
        """Calculate overall truth score from analysis results"""
        try:
            scores = []
            
            # Text analysis score
            if 'text' in analysis:
                text_score = 1 - analysis['text']['fact_check_score']  # Invert score since higher means more likely to be hate speech
                scores.append(text_score)
            
            # Image analysis score
            if 'images' in analysis:
                # Average image scores
                image_scores = [0.8 for _ in analysis['images']]  # Placeholder - implement actual scoring
                scores.append(sum(image_scores) / len(image_scores))
            
            # Video analysis score
            if 'videos' in analysis:
                # Average video scores
                video_scores = [0.7 for _ in analysis['videos']]  # Placeholder - implement actual scoring
                scores.append(sum(video_scores) / len(video_scores))
            
            # Source analysis score
            if 'source' in analysis:
                source_score = 0.7  # Placeholder - implement actual scoring
                scores.append(source_score)
            
            # Calculate weighted average
            weights = [0.4, 0.3, 0.2, 0.1]  # Weights for text, image, video, source
            weighted_sum = sum(score * weight for score, weight in zip(scores, weights[:len(scores)]))
            total_weight = sum(weights[:len(scores)])
            
            return weighted_sum / total_weight if total_weight > 0 else 0.5
            
        except Exception as e:
            logger.error(f"Error in _calculate_truth_score: {str(e)}")
            return 0.5

    def _calculate_confidence(self, analysis: Dict) -> float:
        """Calculate confidence in the analysis"""
        try:
            confidences = []
            
            # Text analysis confidence
            if 'text' in analysis:
                text_conf = 0.8  # Placeholder - implement actual confidence calculation
                confidences.append(text_conf)
            
            # Image analysis confidence
            if 'images' in analysis:
                image_conf = 0.7  # Placeholder - implement actual confidence calculation
                confidences.append(image_conf)
            
            # Video analysis confidence
            if 'videos' in analysis:
                video_conf = 0.6  # Placeholder - implement actual confidence calculation
                confidences.append(video_conf)
            
            # Source analysis confidence
            if 'source' in analysis:
                source_conf = 0.9  # Placeholder - implement actual confidence calculation
                confidences.append(source_conf)
            
            # Calculate weighted average
            weights = [0.4, 0.3, 0.2, 0.1]  # Weights for text, image, video, source
            weighted_sum = sum(conf * weight for conf, weight in zip(confidences, weights[:len(confidences)]))
            total_weight = sum(weights[:len(confidences)])
            
            return weighted_sum / total_weight if total_weight > 0 else 0.5
            
        except Exception as e:
            logger.error(f"Error in _calculate_confidence: {str(e)}")
            return 0.5

    def _extract_video_frames(self, video_url: str, num_frames: int = 10) -> List[str]:
        """Extract frames from video for analysis"""
        try:
            # Download video
            response = requests.get(video_url)
            video_path = self.cache_dir / "temp_video.mp4"
            with open(video_path, 'wb') as f:
                f.write(response.content)
            
            # Open video
            cap = cv2.VideoCapture(str(video_path))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Calculate frame intervals
            frame_interval = total_frames // num_frames
            
            frames = []
            for i in range(num_frames):
                # Set frame position
                cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_interval)
                
                # Read frame
                ret, frame = cap.read()
                if ret:
                    # Save frame
                    frame_path = self.cache_dir / f"frame_{i}.jpg"
                    cv2.imwrite(str(frame_path), frame)
                    frames.append(str(frame_path))
            
            # Clean up
            cap.release()
            video_path.unlink()
            
            return frames
            
        except Exception as e:
            logger.error(f"Error in _extract_video_frames: {str(e)}")
            raise 