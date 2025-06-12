# In your bias_detector.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class BiasDetector:
    def __init__(self):
        self.categories = ['unbiased', 'biased']  # or your categories
        self._load_model()
    
    def _load_model(self):
        try:
            # Use a pre-trained model for bias detection
            model_name = "unitary/toxic-bert"  # or another bias detection model
            # OR
            # model_name = "martin-ha/toxic-comment-model"
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to base model
            self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
            self.model = AutoModelForSequenceClassification.from_pretrained(
                "bert-base-uncased", 
                num_labels=len(self.categories)
            )