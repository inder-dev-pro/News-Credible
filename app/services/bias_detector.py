import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Any, List
import numpy as np
from pathlib import Path

class BiasDetector:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = Path("app/models/bias_model.pt")
        self.tokenizer_path = Path("app/models/bias_tokenizer")
        self.categories = {
            0: "left",
            1: "right", 
            2: "center",
            3: "sensationalist",
            4: "neutral"
        }
        # Initialize model and tokenizer
        self._load_model()
        
        # Define bias categories

        
    def _load_model(self):
        """Load the pre-trained model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            print(f"Error loading model: {e}")
            # Initialize with default model for development
            self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
            self.model = AutoModelForSequenceClassification.from_pretrained(
                "bert-base-uncased",
                num_labels=len(self.categories)
            )
            self.model.to(self.device)
            self.model.eval()

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for bias and return detailed results.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing bias analysis results
        """
        # Tokenize and prepare input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            
        # Get predicted category and confidence
        pred_idx = torch.argmax(probabilities).item()
        confidence = probabilities[0][pred_idx].item()
        
        # Extract keywords (placeholder - implement proper keyword extraction)
        keywords = self._extract_keywords(text)
        
        return {
            "bias_score": float(probabilities[0][pred_idx]),
            "bias_category": self.categories[pred_idx],
            "confidence": confidence,
            "explanation": self._generate_explanation(
                self.categories[pred_idx],
                confidence,
                keywords
            ),
            "keywords": keywords
        }
    
    async def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze multiple texts in batch.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of analysis results
        """
        results = []
        for text in texts:
            result = await self.analyze_text(text)
            results.append(result)
        return results
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract relevant keywords from text.
        This is a placeholder implementation.
        """
        # TODO: Implement proper keyword extraction
        words = text.lower().split()
        return list(set(words))[:5]  # Return first 5 unique words as keywords
    
    def _generate_explanation(
        self,
        category: str,
        confidence: float,
        keywords: List[str]
    ) -> str:
        """
        Generate human-readable explanation of the bias analysis.
        """
        confidence_level = "high" if confidence > 0.8 else "moderate" if confidence > 0.6 else "low"
        
        explanations = {
            "left": f"This content shows {confidence_level} confidence of left-leaning bias. "
                   f"Key terms suggesting this include: {', '.join(keywords)}",
            "right": f"This content shows {confidence_level} confidence of right-leaning bias. "
                    f"Key terms suggesting this include: {', '.join(keywords)}",
            "center": f"This content appears to be relatively balanced with {confidence_level} confidence. "
                     f"The language used is generally neutral and objective.",
            "sensationalist": f"This content shows {confidence_level} confidence of sensationalist tendencies. "
                            f"Key terms suggesting this include: {', '.join(keywords)}",
            "neutral": f"This content appears to be neutral with {confidence_level} confidence. "
                      f"The language used is generally objective and factual."
        }
        
        return explanations.get(category, "Unable to generate explanation.") 