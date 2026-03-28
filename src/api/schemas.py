from pydantic import BaseModel, Field
from typing import Optional, List


class NewsDetectionRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=50000)
    use_llm: bool = False
    use_ml: bool = True
    use_rules: bool = True


class BatchDetectionRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=100)


class TrainingRequest(BaseModel):
    texts: List[str]
    labels: List[str]
    algorithm: str = "logistic"
    test_size: float = Field(default=0.2, ge=0.1, le=0.5)


class HealthResponse(BaseModel):
    status: str
    ml_model_loaded: bool
    llm_available: bool


class DetectionResult(BaseModel):
    ml_prediction: Optional[str] = None
    ml_confidence: Optional[float] = None
    llm_analysis: Optional[dict] = None
    rule_based_result: Optional[dict] = None
    final_verdict: str
    confidence: float
    all_results: dict