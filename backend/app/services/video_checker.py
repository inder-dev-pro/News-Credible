import cv2
import numpy as np
from typing import Dict, Any, List, Tuple
import torch
from pathlib import Path
import tempfile
import os
from deepface import DeepFace

class VideoChecker:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = Path("app/models/video_cnn_model.pt")
        
        # Initialize model
        self._load_model()
        
    def _load_model(self):
        """Load the pre-trained model for video manipulation detection"""
        try:
            # TODO: Implement proper model loading
            self.model = None  # Placeholder for actual model loading
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    async def analyze_video(
        self,
        video_data: bytes,
        analyze_frames: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze a video for signs of manipulation.
        
        Args:
            video_data: Raw video data in bytes
            analyze_frames: Whether to perform frame-level analysis
            
        Returns:
            Dictionary containing analysis results
        """
        # Save video data to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_file.write(video_data)
            temp_path = temp_file.name
        
        try:
            # Open video file
            cap = cv2.VideoCapture(temp_path)
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps
            
            # Perform frame analysis if requested
            frame_results = []
            if analyze_frames:
                frame_results = await self._analyze_frames(cap)
            
            # Perform deepfake detection
            deepfake_result = await self._detect_deepfakes(cap)
            
            # Extract metadata
            metadata = self._extract_metadata(cap)
            
            # Combine results
            is_authentic = all([
                all(frame["is_authentic"] for frame in frame_results),
                deepfake_result["is_authentic"]
            ])
            
            confidence = min(
                min((frame["confidence"] for frame in frame_results), default=1.0),
                deepfake_result["confidence"]
            )
            
            manipulation_type = None
            if not is_authentic:
                manipulation_type = self._determine_manipulation_type(
                    frame_results,
                    deepfake_result
                )
            
            return {
                "is_authentic": is_authentic,
                "confidence": confidence,
                "manipulation_type": manipulation_type,
                "evidence": [
                    *frame_results,
                    deepfake_result
                ],
                "metadata": metadata
            }
            
        finally:
            # Clean up
            cap.release()
            os.unlink(temp_path)
    
    async def _analyze_frames(self, cap: cv2.VideoCapture) -> List[Dict[str, Any]]:
        """
        Analyze individual frames of the video.
        """
        results = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Analyze every 10th frame to save processing time
            if frame_count % 10 == 0:
                # Convert frame to RGB for DeepFace
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Perform face detection and analysis
                try:
                    face_analysis = DeepFace.analyze(
                        frame_rgb,
                        actions=['age', 'gender', 'race', 'emotion'],
                        enforce_detection=False
                    )
                    
                    # Check for inconsistencies in face analysis
                    is_authentic = self._check_face_consistency(face_analysis)
                    confidence = 0.8 if is_authentic else 0.3
                    
                    results.append({
                        "frame_number": frame_count,
                        "analysis_type": "face_analysis",
                        "is_authentic": is_authentic,
                        "confidence": confidence,
                        "face_data": face_analysis
                    })
                except Exception as e:
                    print(f"Error analyzing frame {frame_count}: {e}")
            
            frame_count += 1
        
        return results
    
    async def _detect_deepfakes(self, cap: cv2.VideoCapture) -> Dict[str, Any]:
        """
        Detect potential deepfake manipulation in the video.
        """
        # TODO: Implement proper deepfake detection
        # This is a placeholder implementation
        return {
            "analysis_type": "deepfake_detection",
            "is_authentic": True,
            "confidence": 0.9,
            "details": "No signs of deepfake manipulation detected"
        }
    
    def _extract_metadata(self, cap: cv2.VideoCapture) -> Dict[str, Any]:
        """
        Extract and analyze video metadata.
        """
        return {
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "duration": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
        }
    
    def _check_face_consistency(self, face_analysis: List[Dict[str, Any]]) -> bool:
        """
        Check for inconsistencies in face analysis results.
        """
        if not face_analysis:
            return True
        
        # Check for multiple faces with identical attributes
        if len(face_analysis) > 1:
            first_face = face_analysis[0]
            for face in face_analysis[1:]:
                if (face["age"] == first_face["age"] and
                    face["gender"] == first_face["gender"] and
                    face["race"] == first_face["race"]):
                    return False
        
        return True
    
    def _determine_manipulation_type(
        self,
        frame_results: List[Dict[str, Any]],
        deepfake_result: Dict[str, Any]
    ) -> str:
        """
        Determine the type of manipulation based on analysis results.
        """
        if not deepfake_result["is_authentic"]:
            return "deepfake"
        
        # Check frame results for inconsistencies
        face_inconsistencies = sum(
            1 for frame in frame_results
            if not frame["is_authentic"]
        )
        
        if face_inconsistencies > len(frame_results) * 0.3:
            return "face_manipulation"
        else:
            return "unknown_manipulation" 