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
├── requirements.txt         # Python dependencies (Backend)
├── main.py                  # Backend entry point
├── data/                    # Sample/training data
├── models/                  # Saved ML models
├── src/                     # Backend source
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration loader
│   ├── api/
│   │   ├── routes.py        # REST API endpoints
│   │   └── schemas.py       # Pydantic request/response models
│   ├── preprocessing/
│   │   └── text_preprocessor.py   # NLTK/spaCy text cleaning
│   ├── features/
│   │   ├── fake_news_classifier.py  # ML classifier
│   │   └── feature_extractor.py     # Feature extraction
│   ├── models/
│   │   └── llm_detector.py   # LLM + rule-based detection
│   └── utils/
│       └── data_loader.py   # Data loading utilities
└── ui/                      # Frontend (Flask)
    ├── app/
    │   └── app.py           # Flask application
    ├── templates/
    │   └── index.html       # Main UI template
    ├── static/
    │   ├── css/
    │   │   └── style.css    # Styling
    │   └── js/
    │       └── app.js       # JavaScript
    └── requirements.txt     # UI dependencies
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

## Installation & Setup

### Step 1: Clone the Repository
```bash
cd Fake-News-Detector
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```


### Step 5: (Optional) Configure LLM
Edit `config.yaml` and add your OpenAI API key to enable LLM-based detection:
```yaml
llm:
  api_key: "YOUR-OPENAI-API-KEY"
```

## Running the Application

### Option 1: Run Both Servers Manually

**Terminal 1 - Backend (Port 8000):**
```bash
python main.py
```

**Terminal 2 - UI (Port 5050):**
```bash
cd ui
python app/app.py
```

### Option 2: Run in Background

**Start Backend:**
```bash
python main.py > backend.log 2>&1 &
```

**Start UI:**
```bash
cd ui
python app/app.py > ui.log 2>&1 &
```

### Option 3: Using uvicorn (Backend Only)
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Access the Application

- **Backend API**: http://localhost:8000
- **UI**: http://localhost:5050

Open http://localhost:5050 in your browser to use the Fake News Detector.

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

## Running the Application

### Start Backend (Port 8000)

```bash
# Option 1: Using main.py
python main.py

# Option 2: Using uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Option 3: In background
python main.py > server.log 2>&1 &
```

### Start UI (Port 5050)

```bash
cd ui
python app/app.py

# Or in background
cd ui && python app/app.py > ui.log 2>&1 &
```

The API will be available at:
- **Backend**: http://localhost:8000
- **UI**: http://localhost:5050

### Quick Start (Both Servers)

```bash
# Terminal 1 - Backend
python main.py

# Terminal 2 - UI
cd ui && python app/app.py
```

Then open http://localhost:5050 in your browser.

## API Endpoints

| Endpoint                   | Method | Description           |
| -------------------------- | ------ | --------------------- |
| `/`                        | GET    | API information       |
| `/api/v1/health`           | GET    | Health check          |
| `/api/v1/detect`           | POST   | Detect fake news      |
| `/api/v1/train`            | POST   | Train ML model        |
| `/api/v1/batch-detect`     | POST   | Batch detection       |
| `/api/v1/extract-features` | POST   | Extract text features |
| `/api/v1/model-info`       | GET    | Model information     |

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

## Using the UI

The project includes a user-friendly Flask UI that consumes the backend API.

### Access the UI

Open your browser and navigate to: **http://localhost:5050**

### UI Features

1. **Detect Tab** - Analyze single news articles
   - Enter text and choose detection methods (ML, Rule-based, LLM)
   - View verdict, confidence, and detailed results

2. **Batch Detect Tab** - Analyze multiple articles
   - Enter multiple articles (one per line)
   - View all results in a list

3. **Train Tab** - Train the ML model
   - Enter training data in format: `text|real` or `text|fake` (one per line)
   - Choose algorithm and train
   - View accuracy, precision, recall, F1 score

4. **Features Tab** - Extract linguistic features
   - Enter text to analyze
   - View 20+ extracted features

### Model Status

The bottom of the UI shows:
- ML Model status (Loaded/Not Loaded)
- LLM availability (Available/Not Available)

### API Proxy

The Flask UI proxies all requests to the FastAPI backend at http://localhost:8000. Ensure the backend is running before using the UI.

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

### Backend
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

### UI
- **flask** - Web framework
- **requests** - HTTP client

## Training Data

Sample training data is included in the `data/` folder:

- `data/sample_news.json` - 30 samples (15 real, 15 fake)
- `data/sample_news.csv` - 30 samples in CSV format
- `data/training_data.csv` - 170 samples for model training

Format for training: `text|real` or `text|fake` (one per line)

## License

MIT License
