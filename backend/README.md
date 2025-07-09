# NewsCredible - Bias & Media Authenticity Detector

NewsCredible is an advanced tool for detecting media bias and verifying the authenticity of news content. It combines machine learning, computer vision, and fact-checking to provide comprehensive analysis of news articles, images, and videos.

## Features

- 📝 **Text Bias Detection**: Analyzes news articles for political bias and sensationalism
- 🖼️ **Image Authenticity**: Detects manipulated images using multiple techniques
- 🎥 **Video Verification**: Identifies deepfakes and edited videos
- 🔍 **Fact-Check Integration**: Cross-references claims with fact-checking databases
- 📊 **Trust Score**: Provides a comprehensive credibility assessment

## Project Structure

```
NewsCredible/
├── app/                    # FastAPI backend
├── media_checker/          # Image & video analysis
├── text_bias_model/        # Bias detection models
├── frontend/              # Web interface
├── database/              # Database management
├── scripts/               # Utility scripts
└── tests/                 # Test suite
```

## Setup & Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NewsCredible.git
cd NewsCredible
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python database/db_init.py
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload
```

## Troubleshooting

### TensorFlow Hub Model Loading Issues

If you encounter errors like:
```
Error initializing models: Trying to load a model of incompatible/unknown type
```

This is typically caused by corrupted TensorFlow Hub cache. To resolve:

1. **Automatic Fix**: The application now automatically clears the cache on startup
2. **Manual Fix**: Run the cache clearing script:
```bash
python scripts/clear_tfhub_cache.py
```

3. **Alternative**: If the issue persists, the application will fall back to Gemini-only analysis for images

### Environment Variables

Make sure to set the following environment variables:
- `GOOGLE_API_KEY`: Your Google API key for Gemini integration

## Usage

### Text Bias Detection
```python
import requests

response = requests.post("http://localhost:8000/detect_bias", 
    json={"text": "Your news article text here"})
print(response.json())
```

### Image Verification
```python
import requests

files = {"file": open("image.jpg", "rb")}
response = requests.post("http://localhost:8000/verify_image", files=files)
print(response.json())
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- AllSides and Media Bias/Fact Check for bias labeling data
- FaceForensics++ for deepfake detection datasets
- Various fact-checking organizations for their valuable work 