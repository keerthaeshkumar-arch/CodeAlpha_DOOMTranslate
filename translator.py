"""
DOOM Translate - Core Translation Engine
Provides robust AI-powered language translation, automatic source language detection,
smart text chunking, and fault-tolerant service resilience.
Developed for CodeAlpha Artificial Intelligence Internship.
"""

import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
import requests

try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
except ImportError:
    GoogleTranslator = None
    MyMemoryTranslator = None

import language_data


class TranslationError(Exception):
    """Base exception for DOOM Translate errors."""
    pass


class NetworkError(TranslationError):
    """Raised when network connectivity fails or times out."""
    pass


class RateLimitError(TranslationError):
    """Raised when translation service rate limit is exceeded."""
    pass


class InvalidInputError(TranslationError):
    """Raised when user input fails validation."""
    pass


class LanguageNotSupportedError(TranslationError):
    """Raised when an unsupported language code is requested."""
    pass


@dataclass
class TranslationResult:
    """Encapsulates the complete result and metadata of a translation operation."""
    original_text: str
    translated_text: str
    source_code: str
    source_name: str
    target_code: str
    target_name: str
    detected_code: Optional[str] = None
    detected_name: Optional[str] = None
    timestamp: str = ""
    character_count: int = 0
    word_count: int = 0
    engine_used: str = "Google Neural Translation Engine"

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for session state storage."""
        return asdict(self)


class DOOMTranslator:
    """
    Enterprise-grade translation engine with multi-tier fallback architecture,
    automatic language detection, and intelligent long-text chunking.
    """

    GOOGLE_API_ENDPOINT = "https://translate.googleapis.com/translate_a/single"
    MAX_CHUNK_CHARS = 2500
    REQUEST_TIMEOUT = 12

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "DOOMTranslate/1.0 (CodeAlpha AI Internship; Python 3.12)",
            "Accept": "application/json, text/plain, */*",
        })

    def check_connection(self) -> Dict[str, Any]:
        """
        Performs a live latency and connectivity ping to the translation backend.
        Returns status dictionary with response latency in milliseconds.
        """
        start_time = time.time()
        try:
            params = {
                "client": "gtx",
                "sl": "en",
                "tl": "es",
                "dt": "t",
                "q": "ping"
            }
            response = self._session.get(
                self.GOOGLE_API_ENDPOINT,
                params=params,
                timeout=4
            )
            latency_ms = int((time.time() - start_time) * 1000)

            if response.status_code == 200:
                return {
                    "online": True,
                    "service": "Google Neural Translation Engine",
                    "latency_ms": latency_ms,
                    "message": "Operational & connected"
                }
            elif response.status_code == 429:
                return {
                    "online": False,
                    "service": "Google Neural Translation Engine",
                    "latency_ms": latency_ms,
                    "message": "Rate limit reached on server"
                }
            else:
                return {
                    "online": False,
                    "service": "Google Neural Translation Engine",
                    "latency_ms": latency_ms,
                    "message": f"Server status: HTTP {response.status_code}"
                }
        except requests.exceptions.Timeout:
            return {
                "online": False,
                "service": "Google Neural Translation Engine",
                "latency_ms": None,
                "message": "Connection timed out"
            }
        except requests.exceptions.RequestException as e:
            return {
                "online": False,
                "service": "Google Neural Translation Engine",
                "latency_ms": None,
                "message": f"Network error: {str(e)}"
            }

    def _split_into_chunks(self, text: str) -> List[str]:
        """
        Splits lengthy text into manageable chunks respecting paragraphs and sentences.
        """
        if len(text) <= self.MAX_CHUNK_CHARS:
            return [text]

        chunks = []
        paragraphs = text.split("\n")
        current_chunk = []
        current_length = 0

        for para in paragraphs:
            para_len = len(para) + 1
            if current_length + para_len > self.MAX_CHUNK_CHARS:
                if current_chunk:
                    chunks.append("\n".join(current_chunk))
                    current_chunk = []
                    current_length = 0

                # If a single paragraph is longer than MAX_CHUNK_CHARS, split by sentence
                if len(para) > self.MAX_CHUNK_CHARS:
                    words = para.split(" ")
                    sub_chunk = []
                    sub_len = 0
                    for word in words:
                        if sub_len + len(word) + 1 > self.MAX_CHUNK_CHARS:
                            if sub_chunk:
                                chunks.append(" ".join(sub_chunk))
                                sub_chunk = []
                                sub_len = 0
                        sub_chunk.append(word)
                        sub_len += len(word) + 1
                    if sub_chunk:
                        chunks.append(" ".join(sub_chunk))
                else:
                    current_chunk.append(para)
                    current_length += para_len
            else:
                current_chunk.append(para)
                current_length += para_len

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    def _translate_single_chunk(
        self,
        chunk: str,
        source_code: str,
        target_code: str
    ) -> Tuple[str, Optional[str]]:
        """
        Sends a single chunk to the primary Google Translation engine.
        Returns (translated_text, detected_language_code).
        """
        params = {
            "client": "gtx",
            "sl": source_code,
            "tl": target_code,
            "dt": "t",
            "q": chunk
        }

        try:
            response = self._session.get(
                self.GOOGLE_API_ENDPOINT,
                params=params,
                timeout=self.REQUEST_TIMEOUT
            )
        except requests.exceptions.Timeout:
            raise NetworkError(
                "Translation request timed out. Please check your internet connection."
            )
        except requests.exceptions.ConnectionError:
            raise NetworkError(
                "Unable to connect to translation server. Please check your internet connection."
            )
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error during translation: {str(e)}")

        if response.status_code == 429:
            raise RateLimitError(
                "Translation service rate limit reached. Please wait a few seconds and try again."
            )
        elif response.status_code != 200:
            raise TranslationError(
                f"Translation server returned error status code: {response.status_code}"
            )

        try:
            data = response.json()
        except Exception:
            raise TranslationError("Failed to parse response from translation service.")

        if not data or not isinstance(data, list) or not data[0]:
            raise TranslationError("Empty or malformed response received from translation service.")

        # Join translated segments
        translated_segments = []
        for segment in data[0]:
            if segment and isinstance(segment, list) and len(segment) > 0 and segment[0]:
                translated_segments.append(segment[0])

        translated_text = "".join(translated_segments)

        # Extract detected language
        detected_lang = None
        if len(data) > 2 and data[2] and isinstance(data[2], str):
            detected_lang = data[2]

        return translated_text, detected_lang

    def _fallback_translate(
        self,
        text: str,
        source_code: str,
        target_code: str
    ) -> str:
        """
        Secondary fallback using deep-translator (GoogleTranslator / MyMemory).
        """
        # Try deep-translator GoogleTranslator
        if GoogleTranslator is not None:
            try:
                dt_source = "auto" if source_code == "auto" else source_code
                return GoogleTranslator(source=dt_source, target=target_code).translate(text)
            except Exception:
                pass

        # Try MyMemory fallback
        if MyMemoryTranslator is not None and source_code != "auto":
            try:
                return MyMemoryTranslator(source=source_code, target=target_code).translate(text)
            except Exception:
                pass

        raise TranslationError("All translation services are currently unavailable.")

    def translate(
        self,
        text: str,
        source: str = "auto",
        target: str = "en"
    ) -> TranslationResult:
        """
        Translates text from source language to target language.
        Handles auto-detection, chunking, and validation.

        Args:
            text: Input string to translate.
            source: Source language code (e.g. 'auto', 'en', 'ta', 'hi').
            target: Target language code (e.g. 'ta', 'hi', 'en', 'fr').

        Returns:
            TranslationResult object containing translated text and detailed metadata.
        """
        # 1. Validation: Empty or whitespace text
        if not text or not text.strip():
            raise InvalidInputError("Please enter some text to translate. Input cannot be empty.")

        text_to_translate = text.strip()

        # 2. Validation: Target language cannot be auto
        if target == "auto":
            raise InvalidInputError("Auto Detect cannot be selected as the target language.")

        # 3. Validation: Identical source and target
        if source != "auto" and source == target:
            raise InvalidInputError(
                f"Source and target languages are identical (both set to '{language_data.get_name_by_code(target)}'). "
                "Please select different languages."
            )

        # 4. Validation: Unsupported language codes
        if source != "auto" and not language_data.is_valid_code(source):
            raise LanguageNotSupportedError(f"Unsupported source language code: '{source}'.")
        if not language_data.is_valid_code(target):
            raise LanguageNotSupportedError(f"Unsupported target language code: '{target}'.")

        # 4. Perform translation (with chunking for long text)
        chunks = self._split_into_chunks(text_to_translate)
        translated_chunks = []
        detected_lang_code = None

        for idx, chunk in enumerate(chunks):
            try:
                trans_chunk, chunk_detected = self._translate_single_chunk(
                    chunk=chunk,
                    source_code=source,
                    target_code=target
                )
                translated_chunks.append(trans_chunk)
                if chunk_detected and not detected_lang_code:
                    detected_lang_code = chunk_detected
            except (RateLimitError, NetworkError):
                # If network or rate limit, re-raise directly with user-friendly message
                raise
            except Exception as primary_exc:
                # Attempt fallback engine
                try:
                    fallback_result = self._fallback_translate(
                        chunk,
                        source_code=source,
                        target_code=target
                    )
                    translated_chunks.append(fallback_result)
                except Exception:
                    raise TranslationError(
                        f"Translation engine error: {str(primary_exc)}"
                    )

        final_translated_text = "\n".join(translated_chunks) if len(chunks) > 1 else translated_chunks[0]

        # Resolve language display names
        source_name = language_data.get_name_by_code(source)
        target_name = language_data.get_name_by_code(target)

        detected_code = detected_lang_code if source == "auto" else None
        detected_name = language_data.get_name_by_code(detected_code) if detected_code else None

        return TranslationResult(
            original_text=text_to_translate,
            translated_text=final_translated_text,
            source_code=source,
            source_name=source_name,
            target_code=target,
            target_name=target_name,
            detected_code=detected_code,
            detected_name=detected_name,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            character_count=len(text_to_translate),
            word_count=len(text_to_translate.split()),
            engine_used="DOOM Neural Translation Engine"
        )


# Singleton instance for quick access
default_translator = DOOMTranslator()


def translate_text(text: str, source: str = "auto", target: str = "en") -> TranslationResult:
    """Convenience helper to translate text using the default translator instance."""
    return default_translator.translate(text=text, source=source, target=target)


def check_service_status() -> Dict[str, Any]:
    """Convenience helper to ping the translation service."""
    return default_translator.check_connection()
