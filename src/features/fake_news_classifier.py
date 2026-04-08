from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC, SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
import joblib
import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict
from pathlib import Path


class FakeNewsClassifier:
    def __init__(
        self, model_path: Optional[str] = None, vectorizer_path: Optional[str] = None
    ):
        self.model_path = model_path or "models/classifier.pkl"
        self.vectorizer_path = vectorizer_path or "models/vectorizer.pkl"
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        self._load_model()

    def _load_model(self):
        if Path(self.model_path).exists() and Path(self.vectorizer_path).exists():
            try:
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.is_trained = True
            except Exception:
                pass

    def create_pipeline(self, algorithm: str = "logistic") -> Pipeline:
        vectorizer = TfidfVectorizer(
            max_features=5050,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
        )
        if algorithm == "logistic":
            classifier = LogisticRegression(
                max_iter=1000,
                C=1.0,
                class_weight="balanced",
                random_state=42,
            )
        elif algorithm == "random_forest":
            classifier = RandomForestClassifier(
                n_estimators=200,
                max_depth=20,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1,
            )
        elif algorithm == "naive_bayes":
            classifier = MultinomialNB(alpha=0.1)
        elif algorithm == "svm":
            classifier = SVC(
                C=1.0, class_weight="balanced", max_iter=2000, probability=True
            )
        elif algorithm == "gradient_boost":
            classifier = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42,
            )
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        return Pipeline([("vectorizer", vectorizer), ("classifier", classifier)])

    def train(
        self,
        texts: list,
        labels: list,
        algorithm: str = "logistic",
        test_size: float = 0.2,
    ) -> Dict:
        if len(texts) != len(labels):
            raise ValueError("Texts and labels must have the same length")
        df = pd.DataFrame({"text": texts, "label": labels})
        df = df.dropna()
        X = df["text"].values
        y = df["label"].values
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        pipeline = self.create_pipeline(algorithm)
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(
                precision_score(y_test, y_pred, average="weighted", zero_division=0)
            ),
            "recall": float(
                recall_score(y_test, y_pred, average="weighted", zero_division=0)
            ),
            "f1_score": float(
                f1_score(y_test, y_pred, average="weighted", zero_division=0)
            ),
            "classification_report": classification_report(
                y_test, y_pred, zero_division=0
            ),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        }
        cv_scores = cross_val_score(pipeline, X, y, cv=5)
        metrics["cv_accuracy_mean"] = (
            float(cv_scores.mean()) if not np.isnan(cv_scores.mean()) else 0.0
        )
        metrics["cv_accuracy_std"] = (
            float(cv_scores.std()) if not np.isnan(cv_scores.std()) else 0.0
        )
        self.model = pipeline.named_steps["classifier"]
        self.vectorizer = pipeline.named_steps["vectorizer"]
        self.is_trained = True
        self._save_model()
        return metrics

    def _save_model(self):
        Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)

    def predict(self, text: str) -> Tuple[str, float]:
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        if not text or not isinstance(text, str):
            return "unknown", 0.0
        X = self.vectorizer.transform([text])
        prediction = self.model.predict(X)[0]
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(X)[0]
            confidence = max(proba)
        elif hasattr(self.model, "decision_function"):
            decision = self.model.decision_function(X)[0]
            confidence = 1 / (1 + np.exp(-decision))
        else:
            confidence = 1.0
        return prediction, float(confidence)

    def predict_batch(self, texts: list) -> list:
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        X = self.vectorizer.transform(texts)
        predictions = self.model.predict(X)
        results = []
        for i, pred in enumerate(predictions):
            if hasattr(self.model, "predict_proba"):
                proba = self.model.predict_proba(X[i])[0]
                confidence = max(proba)
            else:
                confidence = 1.0
            results.append({"prediction": pred, "confidence": float(confidence)})
        return results
