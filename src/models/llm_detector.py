from typing import Optional, Dict, List
import json


class LLMDetector:
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.provider = self.config.get("provider", "openai")
        self.model_name = self.config.get("model", "gpt-3.5-turbo")
        self.temperature = self.config.get("temperature", 0.3)
        self.max_tokens = self.config.get("max_tokens", 500)
        self.api_key = self.config.get("api_key", "")
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        if not self.api_key:
            return

        try:
            if self.provider == "openai":
                from openai import OpenAI

                self.client = OpenAI(api_key=self.api_key)

            elif self.provider == "gemini":
                from google import genai

                self.client = genai.Client(api_key=self.api_key)

        except Exception as e:
            print("LLM init error:", e)

    def is_available(self) -> bool:
        return self.client is not None

    def analyze_news(
        self,
        text: str,
        context: Optional[str] = None,
    ) -> Dict:
        if not self.is_available():
            return {
                "available": False,
                "error": "LLM client not initialized. Please provide API key.",
            }
        prompt = self._build_prompt(text, context)
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a fake news detection expert. Analyze the given news article and determine if it appears to be real or fake. Provide a detailed analysis with confidence level.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                result = response.choices[0].message.content
            elif self.provider == "gemini":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
                result = response.text
            return self._parse_response(result)
        except Exception as e:
            return {"available": True, "error": str(e), "analysis": ""}

    def _build_prompt(self, text: str, context: Optional[str] = None) -> str:
        context_str = f"\n\nAdditional context: {context}" if context else ""

        return f"""
                You are a fact-checking system.

                Analyze this news:

                {text}{context_str}

                Instructions:
                - Be precise and objective
                - Do not add extra explanation outside JSON
                - If unsure, return "uncertain"

                Return ONLY valid JSON:

                {{
                "verdict": "real/fake/uncertain",
                "confidence": 0.0-1.0,
                "reasons": [],
                "red_flags": [],
                "supporting_evidence": ""
                }}
                """

    def _parse_response(self, response: str) -> Dict:
        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                parsed = json.loads(json_str)
                parsed.setdefault("available", True)
                return parsed
        except Exception:
            pass
        return {
            "available": True,
            "raw_response": response,
            "verdict": "uncertain",
            "confidence": 0.5,
        }

    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        return [self.analyze_news(text) for text in texts]

    def verify_claim(
        self, claim: str, search_results: Optional[List[str]] = None
    ) -> Dict:
        if not self.is_available():
            return {
                "available": False,
                "error": "LLM client not initialized",
            }
        search_context = ""
        if search_results:
            search_context = "\n\nSearch results:\n" + "\n".join(
                f"- {r}" for r in search_results[:5]
            )
        prompt = f"""Verify the following claim using available information.

Claim: {claim}{search_context}

Provide verdict in JSON:
{{
    "verdict": "true" or "false" or "unverified",
    "confidence": 0.0-1.0,
    "explanation": "brief explanation"
}}"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a fact-checking assistant. Verify claims based on evidence.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            result = response.choices[0].message.content
            return self._parse_response(result)
        except Exception as e:
            return {"available": True, "error": str(e)}


class RuleBasedDetector:
    def __init__(self):
        self.fake_indicators = [
            "clickbait",
            "shocking",
            "you won't believe",
            "breaking",
            "urgent",
            "must share",
            "share now",
            "secret exposed",
            "truth revealed",
            "they don't want you to know",
            "wake up",
            "fake news",
            "hoax",
            "conspiracy",
        ]
        self.trusted_sources = [
            "reuters",
            "ap news",
            "associated press",
            "bbc",
            "npr",
            "pbs",
            "cnn",
            "nbc",
            "abc news",
            "the new york times",
            "the washington post",
            "the wall street journal",
        ]

    def analyze(self, text: str) -> Dict:
        text_lower = text.lower()
        red_flags = []
        score = 0.5
        for indicator in self.fake_indicators:
            if indicator in text_lower:
                red_flags.append(indicator)
                score -= 0.1
        source_indicators = [
            "source:",
            "via @",
            "according to",
            "reports say",
        ]
        has_source = any(s in text_lower for s in source_indicators)
        if has_source:
            score += 0.1
        for trusted in self.trusted_sources:
            if trusted in text_lower:
                score += 0.2
                break
        score = max(0.0, min(1.0, score))
        return {
            "verdict": (
                "fake" if score < 0.4 else "real" if score > 0.6 else "uncertain"
            ),
            "confidence": abs(score - 0.5) * 2,
            "red_flags": red_flags,
            "score": score,
        }
