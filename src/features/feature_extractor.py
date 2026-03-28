import re
import math
from collections import Counter
from typing import Dict, List, Optional
import numpy as np


class FeatureExtractor:
    def __init__(self):
        self.stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
            "been", "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "must", "shall", "can",
            "this", "that", "these", "those", "i", "you", "he", "she", "it", "we",
            "they", "what", "which", "who", "whom", "where", "when", "why", "how",
        }

    def extract_all_features(self, text: str) -> Dict:
        if not text or not isinstance(text, str):
            return {}
        return {
            "length": self.text_length(text),
            "word_count": self.word_count(text),
            "sentence_count": self.sentence_count(text),
            "avg_word_length": self.avg_word_length(text),
            "avg_sentence_length": self.avg_sentence_length(text),
            "capital_ratio": self.capital_ratio(text),
            "digit_ratio": self.digit_ratio(text),
            "special_char_ratio": self.special_char_ratio(text),
            "exclamation_count": self.exclamation_count(text),
            "question_count": self.question_count(text),
            "quote_count": self.quote_count(text),
            "uppercase_word_count": self.uppercase_word_count(text),
            "unique_word_ratio": self.unique_word_ratio(text),
            "punctuation_ratio": self.punctuation_ratio(text),
            "url_count": self.url_count(text),
            "mention_count": self.mention_count(text),
            "hashtag_count": self.hashtag_count(text),
            "readability_score": self.readability_score(text),
            "sentiment_polarity": self.sentiment_polarity(text),
            "entity_density": self.entity_density(text),
        }

    def text_length(self, text: str) -> int:
        return len(text)

    def word_count(self, text: str) -> int:
        words = re.findall(r"\b\w+\b", text)
        return len(words)

    def sentence_count(self, text: str) -> int:
        sentences = re.split(r"[.!?]+", text)
        return len([s for s in sentences if s.strip()])

    def avg_word_length(self, text: str) -> float:
        words = re.findall(r"\b\w+\b", text)
        if not words:
            return 0.0
        return sum(len(w) for w in words) / len(words)

    def avg_sentence_length(self, text: str) -> float:
        sentences = re.split(r"[.!?]+", text)
        sentences = [s for s in sentences if s.strip()]
        if not sentences:
            return 0.0
        words_per_sentence = [len(re.findall(r"\b\w+\b", s)) for s in sentences]
        return sum(words_per_sentence) / len(words_per_sentence)

    def capital_ratio(self, text: str) -> float:
        letters = re.findall(r"[a-zA-Z]", text)
        if not letters:
            return 0.0
        capitals = sum(1 for c in letters if c.isupper())
        return capitals / len(letters)

    def digit_ratio(self, text: str) -> float:
        digits = re.findall(r"\d", text)
        if not text:
            return 0.0
        return len(digits) / len(text)

    def special_char_ratio(self, text: str) -> float:
        special = re.findall(r"[^a-zA-Z0-9\s]", text)
        if not text:
            return 0.0
        return len(special) / len(text)

    def exclamation_count(self, text: str) -> int:
        return text.count("!")

    def question_count(self, text: str) -> int:
        return text.count("?")

    def quote_count(self, text: str) -> int:
        return len(re.findall(r'["\']', text))

    def uppercase_word_count(self, text: str) -> int:
        words = re.findall(r"\b[A-Z]{2,}\b", text)
        return len(words)

    def unique_word_ratio(self, text: str) -> float:
        words = re.findall(r"\b\w+\b", text.lower())
        if not words:
            return 0.0
        return len(set(words)) / len(words)

    def punctuation_ratio(self, text: str) -> float:
        punctuation = re.findall(r"[.,;:!?]", text)
        if not text:
            return 0.0
        return len(punctuation) / len(text)

    def url_count(self, text: str) -> int:
        return len(re.findall(r"http[s]?://\S+", text))

    def mention_count(self, text: str) -> int:
        return len(re.findall(r"@\w+", text))

    def hashtag_count(self, text: str) -> int:
        return len(re.findall(r"#\w+", text))

    def readability_score(self, text: str) -> float:
        words = re.findall(r"\b\w+\b", text)
        sentences = re.split(r"[.!?]+", text)
        sentences = [s for s in sentences if s.strip()]
        if not words or not sentences:
            return 0.0
        avg_words_per_sentence = len(words) / len(sentences)
        syllables = sum(self._count_syllables(w) for w in words)
        avg_syllables_per_word = syllables / len(words) if words else 0
        score = 0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 15.59
        return max(0, min(100, score))

    def _count_syllables(self, word: str) -> int:
        word = word.lower()
        if len(word) <= 3:
            return 1
        vowels = "aeiouy"
        count = 0
        prev_was_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel
        if word.endswith("e"):
            count -= 1
        return max(1, count)

    def sentiment_polarity(self, text: str) -> float:
        positive_words = {
            "good", "great", "excellent", "amazing", "wonderful", "fantastic",
            "love", "best", "perfect", "happy", "beautiful", "awesome",
            "positive", "success", "win", "victory", "hope", "trust", "truth",
        }
        negative_words = {
            "bad", "terrible", "horrible", "worst", "hate", "fake", "false",
            "lie", "deception", "scam", "fraud", "wrong", "evil", "danger",
            "threat", "fear", "worried", "angry", "sad", "fail", "failure",
        }
        words = re.findall(r"\b\w+\b", text.lower())
        positive_count = sum(1 for w in words if w in positive_words)
        negative_count = sum(1 for w in words if w in negative_words)
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        return (positive_count - negative_count) / total

    def entity_density(self, text: str) -> float:
        words = re.findall(r"\b\w+\b", text)
        proper_nouns = re.findall(r"\b[A-Z][a-z]+\b", text)
        if not words:
            return 0.0
        return len(proper_nouns) / len(words)

    def get_feature_vector(self, text: str) -> np.ndarray:
        features = self.extract_all_features(text)
        return np.array(list(features.values()))

    def get_feature_names(self) -> List[str]:
        return [
            "length", "word_count", "sentence_count", "avg_word_length",
            "avg_sentence_length", "capital_ratio", "digit_ratio",
            "special_char_ratio", "exclamation_count", "question_count",
            "quote_count", "uppercase_word_count", "unique_word_ratio",
            "punctuation_ratio", "url_count", "mention_count", "hashtag_count",
            "readability_score", "sentiment_polarity", "entity_density",
        ]