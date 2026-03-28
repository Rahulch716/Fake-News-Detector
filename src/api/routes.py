from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from src.api.schemas import (
    NewsDetectionRequest,
    BatchDetectionRequest,
    TrainingRequest,
    HealthResponse,
    DetectionResult,
)
from src.preprocessing.text_preprocessor import TextPreprocessor
from src.features.fake_news_classifier import FakeNewsClassifier
from src.features.feature_extractor import FeatureExtractor
from src.models.llm_detector import LLMDetector, RuleBasedDetector
from src.config import config

router = APIRouter()

preprocessor = TextPreprocessor(config=config.get("nlp", {}))
classifier = FakeNewsClassifier(
    model_path=config.get("model", {}).get("ml_model_path", "models/classifier.pkl"),
    vectorizer_path=config.get("model", {}).get("vectorizer_path", "models/vectorizer.pkl"),
)
feature_extractor = FeatureExtractor()
llm_detector = LLMDetector(config=config.get("llm", {}))
rule_detector = RuleBasedDetector()


def _combine_results(
    ml_pred: Optional[str], ml_conf: Optional[float], llm_result: Optional[dict], rule_result: Optional[dict]
) -> tuple:
    votes = []
    weights = []
    if ml_pred and ml_conf:
        label = "fake" if ml_pred in ["fake", "0", "FAKE"] else "real"
        votes.append(label)
        weights.append(ml_conf)
    if llm_result and llm_result.get("available"):
        verdict = llm_result.get("verdict", "uncertain")
        if verdict in ["fake", "real", "true", "false"]:
            label = "fake" if verdict in ["fake", "false"] else "real"
            conf = llm_result.get("confidence", 0.5)
            votes.append(label)
            weights.append(conf)
    if rule_result:
        verdict = rule_result.get("verdict", "uncertain")
        if verdict in ["fake", "real"]:
            votes.append(verdict)
            weights.append(rule_result.get("confidence", 0.5))
    if not votes:
        return "unable to determine", 0.0
    weighted_sum = sum(w for v, w in zip(votes, weights) if v == "fake") / sum(weights)
    final_verdict = "fake" if weighted_sum > 0.5 else "real"
    confidence = abs(weighted_sum - 0.5) * 2
    return final_verdict, confidence


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        ml_model_loaded=classifier.is_trained,
        llm_available=llm_detector.is_available(),
    )


@router.post("/detect", response_model=DetectionResult)
async def detect_fake_news(request: NewsDetectionRequest):
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text too short")
    all_results = {}
    ml_prediction = None
    ml_confidence = None
    if request.use_ml and classifier.is_trained:
        try:
            preprocessed_text = preprocessor.preprocess(request.text)
            ml_prediction, ml_confidence = classifier.predict(preprocessed_text)
            all_results["ml"] = {
                "prediction": ml_prediction,
                "confidence": ml_confidence,
            }
        except Exception as e:
            all_results["ml_error"] = str(e)
    llm_analysis = None
    if request.use_llm and llm_detector.is_available():
        try:
            llm_analysis = llm_detector.analyze_news(request.text)
            all_results["llm"] = llm_analysis
        except Exception as e:
            all_results["llm_error"] = str(e)
    rule_result = None
    if request.use_rules:
        try:
            rule_result = rule_detector.analyze(request.text)
            all_results["rule_based"] = rule_result
        except Exception as e:
            all_results["rule_error"] = str(e)
    final_verdict, confidence = _combine_results(
        ml_prediction, ml_confidence, llm_analysis, rule_result
    )
    return DetectionResult(
        ml_prediction=ml_prediction,
        ml_confidence=ml_confidence,
        llm_analysis=llm_analysis,
        rule_based_result=rule_result,
        final_verdict=final_verdict,
        confidence=confidence,
        all_results=all_results,
    )


@router.post("/batch-detect")
async def batch_detect(request: BatchDetectionRequest):
    results = []
    for text in request.texts:
        if len(text.strip()) < 10:
            results.append({"error": "Text too short", "text": text[:50]})
            continue
        try:
            preprocessed = preprocessor.preprocess(text)
            if classifier.is_trained:
                pred, conf = classifier.predict(preprocessed)
            else:
                pred, conf = "unknown", 0.0
            rule_result = rule_detector.analyze(text)
            results.append(
                {
                    "prediction": pred,
                    "confidence": conf,
                    "rule_based": rule_result,
                }
            )
        except Exception as e:
            results.append({"error": str(e)})
    return {"results": results, "total": len(results)}


@router.post("/train")
async def train_model(request: TrainingRequest):
    if len(request.texts) != len(request.labels):
        raise HTTPException(status_code=400, detail="Texts and labels length mismatch")
    if len(request.texts) < 10:
        raise HTTPException(status_code=400, detail="Need at least 10 samples")
    try:
        preprocessed_texts = [preprocessor.preprocess(t) for t in request.texts]
        metrics = classifier.train(
            texts=preprocessed_texts,
            labels=request.labels,
            algorithm=request.algorithm,
            test_size=request.test_size,
        )
        return {"status": "success", "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model-info")
async def model_info():
    return {
        "ml_model_loaded": classifier.is_trained,
        "llm_available": llm_detector.is_available(),
        "algorithms_available": [
            "logistic",
            "random_forest",
            "naive_bayes",
            "svm",
            "gradient_boost",
        ],
    }


@router.post("/extract-features")
async def extract_features(request: Dict):
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text required")
        raise HTTPException(status_code=400, detail="Text required")
    features = feature_extractor.extract_all_features(text)
    return {"features": features}