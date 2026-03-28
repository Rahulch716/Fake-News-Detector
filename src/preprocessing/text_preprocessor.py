import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from typing import Optional

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)
    nltk.download("punkt_tab", quiet=True)
except Exception:
    pass

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

if SPACY_AVAILABLE:
    try:
        SPACY_MODEL = spacy.load("en_core_web_sm")
    except Exception:
        SPACY_MODEL = None


class TextPreprocessor:
    def __init__(self, use_spacy: bool = True, config: Optional[dict] = None):
        self.use_spacy = use_spacy and SPACY_AVAILABLE and SPACY_MODEL is not None
        self.config = config or {}
        self.remove_stopwords = self.config.get("remove_stopwords", True)
        self.remove_punctuation = self.config.get("remove_punctuation", True)
        self.lowercase = self.config.get("lowercase", True)
        self.lemmatize = True
        self.max_length = self.config.get("max_text_length", 10000)
        self.min_length = self.config.get("min_text_length", 10)

    def clean_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        text = text[: self.max_length]
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"http[s]?://\S+", "", text)
        text = re.sub(r"@\w+", "", text)
        text = re.sub(r"#\w+", "", text)
        if self.lowercase:
            text = text.lower()
        text = re.sub(r"[^\w\s]", " " if self.remove_punctuation else "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text: str) -> list:
        if self.use_spacy:
            doc = SPACY_MODEL(text)
            return [token.text for token in doc if not token.is_stop]
        try:
            return word_tokenize(text)
        except Exception:
            return text.split()

    def remove_stop_words(self, tokens: list) -> list:
        if self.remove_stopwords:
            return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]
        return tokens

    def lemmatize_tokens(self, tokens: list) -> list:
        if self.lemmatize:
            return [LEMMATIZER.lemmatize(token) for token in tokens]
        return tokens

    def preprocess(self, text: str) -> str:
        if not text or len(text.strip()) < self.min_length:
            return ""
        text = self.clean_text(text)
        tokens = self.tokenize(text)
        tokens = self.remove_stop_words(tokens)
        tokens = self.lemmatize_tokens(tokens)
        return " ".join(tokens)

    def extract_entities(self, text: str) -> dict:
        if not self.use_spacy or not text:
            return {}
        doc = SPACY_MODEL(text)
        return {
            "entities": [
                {"text": ent.text, "label": ent.label_} for ent in doc.ents
            ],
            "noun_chunks": [chunk.text for chunk in doc.noun_chunks],
        }