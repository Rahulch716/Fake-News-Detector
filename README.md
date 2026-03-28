# Fake News Detector

A backend API for detecting fake news using machine learning, LLM integration, and rule-based heuristics. Built with FastAPI, scikit-learn, NLTK, and spaCy.

## Overview

This project provides a REST API for fake news detection that combines multiple detection approaches:

1. **Machine Learning Classifier** - TF-IDF based text classification using various ML algorithms
2. **LLM Integration** - OpenAI GPT-based analysis for nuanced detection
3. **Rule-Based Detection** - Heuristic analysis for clickbait and suspicious patterns
4. **Feature Extraction** - 20+ linguistic features for detailed text analysis

## Architecture

```
Fake-News-Detector/
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
├── main.py                  # Entry point
├── data/                    # Sample/training data
├── models/                  # Saved ML models
└── src/
    ├── main.py              # FastAPI application
    ├── config.py            # Configuration loader
    ├── api/
    │   ├── routes.py        # REST API endpoints
    │   └── schemas.py       # Pydantic request/response models
    ├── preprocessing/
    │   └── text_preprocessor.py   # NLTK/spaCy text cleaning
    ├── features/
    │   ├── fake_news_classifier.py  # ML classifier
    │   └── feature_extractor.py     # Feature extraction
    ├── models/
    │   └── llm_detector.py   # LLM + rule-based detection
    └── utils/
        └── data_loader.py   # Data loading utilities
```

## Features

### Text Preprocessing
- HTML tag removal
- URL, mention, hashtag detection
- Lowercase conversion
- Stopword removal (NLTK)
- Tokenization (NLTK/spaCy)
- Lemmatization (WordNet)
- spaCy NER support

### ML Classification
Algorithms supported:
- Logistic Regression
- Random Forest
- Naive Bayes
- Support Vector Machine (SVM)
- Gradient Boosting

### Feature Extraction
- Text length, word count, sentence count
- Average word/sentence length
- Capital ratio, digit ratio
- Punctuation analysis
- URL/mention/hashtag counts
- Readability scores (Flesch-Kincaid)
- Sentiment polarity
- Entity density

### Detection Methods
- ML-based classification
- LLM-based analysis (OpenAI GPT)
- Rule-based heuristics (clickbait detection)

## Installation

1. Clone the repository:
```bash
cd Fake-News-Detector
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

5. (Optional) Download NLTK data:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

## Configuration

Edit `config.yaml` to customize:

```yaml
app_name: "Fake News Detector API"
version: "1.0.0"

api:
  host: "0.0.0.0"
  port: 8000
  cors_origins: ["*"]

model:
  ml_model_path: "models/classifier.pkl"
  vectorizer_path: "models/vectorizer.pkl"
  confidence_threshold: 0.6

llm:
  provider: "openai"
  model: "gpt-3.5-turbo"
  temperature: 0.3
  max_tokens: 500
  api_key: "YOUR-API-KEY-HERE"  # Set your OpenAI API key

nlp:
  use_spacy: true
  language: "en"
  remove_stopwords: true
  remove_punctuation: true
  lowercase: true

preprocessing:
  max_text_length: 10000
  min_text_length: 10
```

## Running the Server

### Development Mode (with auto-reload):
```bash
python main.py
```

### Using uvicorn directly:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### In background:
```bash
python main.py > server.log 2>&1 &
```

The API will be available at `http://localhost:8000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/api/v1/health` | GET | Health check |
| `/api/v1/detect` | POST | Detect fake news |
| `/api/v1/train` | POST | Train ML model |
| `/api/v1/batch-detect` | POST | Batch detection |
| `/api/v1/extract-features` | POST | Extract text features |
| `/api/v1/model-info` | GET | Model information |

### Example Usage

#### 1. API Info (GET /)
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "name": "Fake News Detector API",
  "version": "1.0.0",
  "status": "running"
}
```

#### 2. Health Check (GET /api/v1/health)
```bash
curl http://localhost:8000/api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "ml_model_loaded": true,
  "llm_available": false
}
```

#### 3. Model Info (GET /api/v1/model-info)
```bash
curl http://localhost:8000/api/v1/model-info
```

**Response:**
```json
{
  "ml_model_loaded": true,
  "llm_available": false,
  "algorithms_available": [
    "logistic",
    "random_forest",
    "naive_bayes",
    "svm",
    "gradient_boost"
  ]
}
```

#### 4. Detect Fake News (POST /api/v1/detect)

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Scientists discover new breakthrough in renewable energy technology that could change the world.",
    "use_ml": true,
    "use_rules": true
  }'
```

**Response:**
```json
{
  "ml_prediction": "real",
  "ml_confidence": 0.5776844597636563,
  "llm_analysis": null,
  "rule_based_result": {
    "verdict": "uncertain",
    "confidence": 0.0,
    "red_flags": [],
    "score": 0.5
  },
  "final_verdict": "real",
  "confidence": 1.0,
  "all_results": {
    "ml": {
      "prediction": "real",
      "confidence": 0.5776844597636563
    },
    "rule_based": {
      "verdict": "uncertain",
      "confidence": 0.0,
      "red_flags": [],
      "score": 0.5
    }
  }
}
```

**Fake News Detection Example:**
```bash
curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Clickbait: You wont believe what the government is hiding from you! Secret exposed!",
    "use_ml": true,
    "use_rules": true
  }'
```

**Response:**
```json
{
  "ml_prediction": "fake",
  "ml_confidence": 0.5933213759177399,
  "llm_analysis": null,
  "rule_based_result": {
    "verdict": "fake",
    "confidence": 0.4,
    "red_flags": ["clickbait", "secret exposed"],
    "score": 0.3
  },
  "final_verdict": "fake",
  "confidence": 1.0,
  "all_results": {
    "ml": {
      "prediction": "fake",
      "confidence": 0.5933213759177399
    },
    "rule_based": {
      "verdict": "fake",
      "confidence": 0.4,
      "red_flags": ["clickbait", "secret exposed"],
      "score": 0.3
    }
  }
}
```

#### 5. Train Model (POST /api/v1/train)

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/train \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Scientists discover new species in Amazon rainforest",
      "You wont believe what this celebrity did",
      "Breaking: Government announces new policy",
      "Secret exposed: What they dont want you to know",
      "Local team wins championship in exciting match",
      "Clickbait: 10 things you need to know today",
      "Health officials recommend regular exercise",
      "Fake news article spread through social media",
      "Stock market closes at record high",
      "Unverified conspiracy theory goes viral"
    ],
    "labels": ["real", "fake", "real", "fake", "real", "fake", "real", "fake", "real", "fake"],
    "algorithm": "logistic"
  }'
```

**Response:**
```json
{
  "status": "success",
  "metrics": {
    "accuracy": 0.5,
    "precision": 0.25,
    "recall": 0.5,
    "f1_score": 0.3333333333333333,
    "classification_report": "              precision    recall  f1-score   support\n\n        fake       0.00      0.00      0.00         1\n        real       0.50      1.00      0.67         1\n\n    accuracy                           0.50         2\n   macro avg       0.25      0.50      0.33         2\nweighted avg       0.25      0.50      0.33         2",
    "confusion_matrix": [[0, 1], [0, 1]],
    "cv_accuracy_mean": 0.8,
    "cv_accuracy_std": 0.2449489742783178
  }
}
```

#### 6. Extract Features (POST /api/v1/extract-features)

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/extract-features \
  -H "Content-Type: application/json" \
  -d '{"text": "Scientists discover new breakthrough in renewable energy technology."}'
```

**Response:**
```json
{
  "features": {
    "length": 68,
    "word_count": 8,
    "sentence_count": 1,
    "avg_word_length": 7.5,
    "avg_sentence_length": 8.0,
    "capital_ratio": 0.016666666666666666,
    "digit_ratio": 0.0,
    "special_char_ratio": 0.014705882352941176,
    "exclamation_count": 0,
    "question_count": 0,
    "quote_count": 0,
    "uppercase_word_count": 0,
    "unique_word_ratio": 1.0,
    "punctuation_ratio": 0.014705882352941176,
    "url_count": 0,
    "mention_count": 0,
    "hashtag_count": 0,
    "readability_score": 15.555000000000003,
    "sentiment_polarity": 0.0,
    "entity_density": 0.125
  }
}
```

#### 7. Batch Detect (POST /api/v1/batch-detect)

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/batch-detect \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Real news: Scientists find new cure for disease",
      "Clickbait: You wont believe this shocking secret!",
      "Stock market updates for today"
    ]
  }'
```

**Response:**
```json
{
  "results": [
    {
      "prediction": "real",
      "confidence": 0.55,
      "rule_based": {
        "verdict": "uncertain",
        "confidence": 0.0,
        "red_flags": [],
        "score": 0.5
      }
    },
    {
      "prediction": "fake",
      "confidence": 0.59,
      "rule_based": {
        "verdict": "fake",
        "confidence": 0.4,
        "red_flags": ["clickbait"],
        "score": 0.3
      }
    },
    {
      "prediction": "real",
      "confidence": 0.5,
      "rule_based": {
        "verdict": "uncertain",
        "confidence": 0.0,
        "red_flags": [],
        "score": 0.5
      }
    }
  ],
  "total": 3
}
```

## Request/Response Schema

### Detect Request
```json
{
  "text": "string (required, min 10 chars)",
  "use_ml": true,
  "use_llm": false,
  "use_rules": true
}
```

### Detect Response
```json
{
  "ml_prediction": "real" | "fake" | null,
  "ml_confidence": 0.0-1.0,
  "llm_analysis": { ... } | null,
  "rule_based_result": {
    "verdict": "real" | "fake" | "uncertain",
    "confidence": 0.0-1.0,
    "red_flags": ["clickbait", "secret exposed", ...],
    "score": 0.0-1.0
  },
  "final_verdict": "real" | "fake" | "unable to determine",
  "confidence": 0.0-1.0,
  "all_results": { ... }
}
```

### Train Request
```json
{
  "texts": ["text1", "text2", ...],
  "labels": ["real", "fake", ...],
  "algorithm": "logistic" | "random_forest" | "naive_bayes" | "svm" | "gradient_boost",
  "test_size": 0.2
}
```

## Using with UI

The backend is designed to work with any UI. To integrate:

1. Start the server: `python main.py`
2. Make HTTP requests to `http://localhost:8000/api/v1/detect`
3. Pass JSON body with `text` field and optional `use_ml`, `use_llm`, `use_rules` flags

## How It Works

### Detection Pipeline

1. **Input Processing**: Raw text is cleaned and preprocessed
2. **Feature Extraction**: Text is converted to TF-IDF vectors + linguistic features
3. **Multi-Method Detection**:
   - ML model predicts class (real/fake) with confidence
   - LLM provides detailed analysis (if API key configured)
   - Rule-based detector checks for clickbait patterns
4. **Result Aggregation**: Weighted voting combines all methods
5. **Output**: Returns verdict, confidence, and detailed results

### Training Pipeline

1. Collect labeled news articles (real/fake)
2. Preprocess text (clean, tokenize, lemmatize)
3. Train ML model with TF-IDF vectorization
4. Evaluate with cross-validation
5. Save model for future predictions

## Dependencies

- **fastapi** - Modern Python web framework
- **uvicorn** - ASGI server
- **scikit-learn** - ML library
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **nltk** - Natural language toolkit
- **spacy** - Industrial NLP
- **pydantic** - Data validation
- **joblib** - Model serialization
- **pyyaml** - Config parsing

## License

MIT License
