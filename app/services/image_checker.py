import cv2
import numpy as np
from PIL import Image
import io
from typing import Dict, Any, List, Tuple
import torch
from pathlib import Path
from app.services.reverse_search import ReverseImageSearch

class ImageChecker:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = Path("app/models/image_cnn_model.pt")
        self.reverse_search = ReverseImageSearch()
        
        # Initialize model
        self._load_model()
        
    def _load_model(self):
        """Load the pre-trained CNN model for image manipulation detection"""
        try:
            # TODO: Implement proper model loading
            self.model = None  # Placeholder for actual model loading
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    async def analyze_image(
        self,
        image_data: bytes,
        perform_reverse_search: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze an image for signs of manipulation.
        
        Args:
            image_data: Raw image data in bytes
            perform_reverse_search: Whether to perform reverse image search
            
        Returns:
            Dictionary containing analysis results
        """
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_data))
        
        # Perform various analyses
        ela_result = self._error_level_analysis(image)
        noise_result = self._noise_analysis(image)
        metadata = self._extract_metadata(image)
        
        # Perform reverse image search if requested
        reverse_search_results = []
        if perform_reverse_search:
            reverse_search_results = await self.reverse_search.search(image_data)
        
        # Combine results
        is_authentic = all([
            ela_result["is_authentic"],
            noise_result["is_authentic"]
        ])
        
        confidence = min(
            ela_result["confidence"],
            noise_result["confidence"]
        )
        
        manipulation_type = None
        if not is_authentic:
            manipulation_type = self._determine_manipulation_type(
                ela_result,
                noise_result
            )
        
        return {
            "is_authentic": is_authentic,
            "confidence": confidence,
            "manipulation_type": manipulation_type,
            "evidence": [
                ela_result,
                noise_result,
                *reverse_search_results
            ],
            "metadata": metadata
        }
    
    def _error_level_analysis(self, image: Image.Image) -> Dict[str, Any]:
        """
        Perform Error Level Analysis (ELA) on the image.
        """
        # Convert PIL Image to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Save with specific JPEG quality
        temp_path = "temp_ela.jpg"
        cv2.imwrite(temp_path, cv_image, [cv2.IMWRITE_JPEG_QUALITY, 90])
        
        # Read the compressed image
        compressed = cv2.imread(temp_path)
        
        # Calculate difference
        diff = cv2.absdiff(cv_image, compressed)
        
        # Calculate statistics
        mean_diff = np.mean(diff)
        std_diff = np.std(diff)
        
        # Determine if image is likely manipulated
        is_authentic = mean_diff < 5.0 and std_diff < 10.0
        confidence = 1.0 - min(mean_diff / 10.0, 1.0)
        
        return {
            "analysis_type": "error_level",
            "is_authentic": is_authentic,
            "confidence": confidence,
            "mean_difference": float(mean_diff),
            "std_difference": float(std_diff)
        }
    
    def _noise_analysis(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze noise patterns in the image.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        
        # Apply noise detection
        noise = cv2.fastNlMeansDenoising(gray)
        diff = cv2.absdiff(gray, noise)
        
        # Calculate statistics
        mean_noise = np.mean(diff)
        std_noise = np.std(diff)
        
        # Determine if noise pattern is consistent
        is_authentic = std_noise < 15.0
        confidence = 1.0 - min(std_noise / 20.0, 1.0)
        
        return {
            "analysis_type": "noise_pattern",
            "is_authentic": is_authentic,
            "confidence": confidence,
            "mean_noise": float(mean_noise),
            "std_noise": float(std_noise)
        }
    
    def _extract_metadata(self, image: Image.Image) -> Dict[str, Any]:
        """
        Extract and analyze image metadata.
        """
        metadata = {}
        
        # Extract EXIF data
        exif = image._getexif()
        if exif:
            for tag_id in exif:
                tag = Image.TAGS.get(tag_id, tag_id)
                data = exif.get(tag_id)
                if isinstance(data, bytes):
                    data = data.decode()
                metadata[tag] = data
        
        # Add basic image information
        metadata.update({
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height
        })
        
        return metadata
    
    def _determine_manipulation_type(
        self,
        ela_result: Dict[str, Any],
        noise_result: Dict[str, Any]
    ) -> str:
        """
        Determine the type of manipulation based on analysis results.
        """
        if ela_result["mean_difference"] > 10.0:
            return "content_manipulation"
        elif noise_result["std_noise"] > 20.0:
            return "noise_inconsistency"
        else:
            return "unknown_manipulation" 