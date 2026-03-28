import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple


def load_sample_data(data_path: str = "data/sample_news.csv") -> Tuple[list, list]:
    path = Path(data_path)
    if not path.exists():
        sample_data = {
            "text": [
                "Scientists discover new species in Amazon rainforest",
                "You won't believe what this celebrity did",
                "Breaking: Government announces new policy",
                "Secret exposed: What they don't want you to know",
                "Local team wins championship in exciting match",
                "Clickbait: 10 things you need to know today",
                "Health officials recommend regular exercise",
                "Fake news article spread through social media",
                "Stock market closes at record high",
                "Unverified conspiracy theory goes viral",
            ],
            "label": [
                "real",
                "fake",
                "real",
                "fake",
                "real",
                "fake",
                "real",
                "fake",
                "real",
                "fake",
            ],
        }
        df = pd.DataFrame(sample_data)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        return sample_data["text"], sample_data["label"]
    df = pd.read_csv(path)
    return df["text"].tolist(), df["label"].tolist()


def load_csv_data(
    file_path: str, text_column: str = "text", label_column: str = "label"
) -> Tuple[list, list]:
    df = pd.read_csv(file_path)
    if text_column not in df.columns or label_column not in df.columns:
        raise ValueError(f"Columns {text_column} or {label_column} not found")
    df = df.dropna(subset=[text_column, label_column])
    return df[text_column].tolist(), df[label_column].tolist()


def load_json_data(file_path: str) -> Tuple[list, list]:
    import json

    with open(file_path, "r") as f:
        data = json.load(f)
    texts = [item["text"] for item in data if "text" in item]
    labels = [item.get("label", item.get("label", "unknown")) for item in data]
    return texts, labels


def prepare_training_data(raw_data: list, labels: list) -> Tuple[list, list]:
    clean_texts = []
    clean_labels = []
    for text, label in zip(raw_data, labels):
        if isinstance(text, str) and len(text.strip()) > 10:
            clean_texts.append(text)
            clean_labels.append(label)
    return clean_texts, clean_labels


if __name__ == "__main__":
    texts, labels = load_sample_data()
    print(f"Loaded {len(texts)} sample articles")
    print(f"Real: {labels.count('real')}, Fake: {labels.count('fake')}")