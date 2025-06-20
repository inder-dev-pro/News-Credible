# NewsCredible

NewsCredible is an AI-powered platform for analyzing the credibility, bias, and factual accuracy of news articles. The core of the project is the **Article Analyzer**, which leverages advanced machine learning and NLP models to provide in-depth content analysis, helping users identify misinformation and bias in news content.

## 🚀 Main Features

- **Article Analyzer**: Analyze news articles for bias, credibility, and factual accuracy using state-of-the-art AI models.
- **Content Analysis API**: FastAPI backend exposes endpoints for content analysis, fact-checking, and media verification.
- **Bias Detection**: Detects potential bias in text using custom and pre-trained models.
- **Fact-Check Lookup**: Cross-references claims with fact-checking databases.
- **Media Verification**: Tools for verifying images and videos in news articles.

## 🗂️ Project Structure

```
NewsCredible/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entrypoint
│   │   ├── routers/
│   │   │   ├── content.py         # Article/content analysis endpoints
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── content_analyzer.py # Core logic for article analysis
│   │   │   └── ...
│   │   └── models/
│   │       └── bias_tokenizer.py
│   └── ...
├── frontend/
│   └── src/
│       ├── components/
│       │   └── ArticleAnalyzerTool.tsx # Main UI for article analysis
│       └── pages/
│           └── ArticleAnalyzer.tsx     # Article Analyzer page
└── ...
```

## 🧠 Article Analyzer (Core Focus)

The **Article Analyzer** is the centerpiece of NewsCredible. It allows users to submit news articles and receive:
- Bias and sentiment analysis
- Fact-checking results
- Media (image/video) verification
- Detailed credibility scoring

The backend logic is primarily in `backend/app/services/content_analyzer.py` and exposed via the `/api/v1/content` endpoints in `backend/app/routers/content.py`.

The frontend provides an interactive UI in `frontend/src/components/ArticleAnalyzerTool.tsx` and `frontend/src/pages/ArticleAnalyzer.tsx`.

## 🛠️ Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- (Optional) Docker

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker (Full Stack)
```bash
docker build -t newscredible .
docker run -p 8000:8000 newscredible
```

## 📚 API Overview

- `POST /api/v1/content/analyze` — Analyze an article for bias, credibility, and facts
- `GET /api/v1/content/summary` — Get a summary of an article
- See `backend/app/routers/content.py` for all endpoints

## 🤝 Contributing

1. Fork the repo and create your branch (`git checkout -b feature/your-feature`)
2. Commit your changes (`git commit -am 'Add new feature'`)
3. Push to the branch (`git push origin feature/your-feature`)
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

---

**NewsCredible** — Empowering readers with AI-driven news analysis. 