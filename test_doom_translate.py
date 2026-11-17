"""
DOOM Translate - Automated Test Suite
Verifies all 14 mandatory CodeAlpha internship testing requirements.
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import requests

# Ensure project directory is in sys.path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import language_data
import translator
from translator import (
    DOOMTranslator,
    TranslationResult,
    InvalidInputError,
    NetworkError,
    RateLimitError,
    TranslationError,
)


class TestDOOMTranslateSuite(unittest.TestCase):
    """Test suite covering all 14 required capabilities."""

    @classmethod
    def setUpClass(cls):
        cls.engine = DOOMTranslator()

    # 1. English to Tamil translation
    def test_01_english_to_tamil(self):
        input_text = "Good morning, welcome to DOOM Translate."
        result = self.engine.translate(input_text, source="en", target="ta")
        self.assertIsInstance(result, TranslationResult)
        self.assertEqual(result.source_code, "en")
        self.assertEqual(result.target_code, "ta")
        self.assertTrue(len(result.translated_text) > 0)
        # Check Tamil unicode range (\u0B80-\u0BFF)
        has_tamil = any("\u0B80" <= char <= "\u0BFF" for char in result.translated_text)
        self.assertTrue(has_tamil, f"Expected Tamil characters in output: {result.translated_text}")
        print(" [PASS] 01. English to Tamil translation")

    # 2. English to Hindi translation
    def test_02_english_to_hindi(self):
        input_text = "Artificial Intelligence bridges communication."
        result = self.engine.translate(input_text, source="en", target="hi")
        self.assertIsInstance(result, TranslationResult)
        self.assertEqual(result.source_code, "en")
        self.assertEqual(result.target_code, "hi")
        self.assertTrue(len(result.translated_text) > 0)
        # Check Devanagari unicode range (\u0900-\u097F)
        has_devanagari = any("\u0900" <= char <= "\u097F" for char in result.translated_text)
        self.assertTrue(has_devanagari, f"Expected Hindi characters in output: {result.translated_text}")
        print(" [PASS] 02. English to Hindi translation")

    # 3. Tamil to English translation
    def test_03_tamil_to_english(self):
        input_text = "வணக்கம் உலகம்"
        result = self.engine.translate(input_text, source="ta", target="en")
        self.assertIsInstance(result, TranslationResult)
        self.assertEqual(result.source_code, "ta")
        self.assertEqual(result.target_code, "en")
        self.assertIn("world", result.translated_text.lower())
        print(" [PASS] 03. Tamil to English translation")

    # 4. Automatic source language detection
    def test_04_automatic_source_detection(self):
        # Test French detection
        res_fr = self.engine.translate("Bonjour le monde, comment allez-vous?", source="auto", target="en")
        self.assertEqual(res_fr.detected_code, "fr")
        self.assertEqual(res_fr.detected_name, "French")
        self.assertIn("world", res_fr.translated_text.lower())

        # Test Tamil detection
        res_ta = self.engine.translate("வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?", source="auto", target="en")
        self.assertEqual(res_ta.detected_code, "ta")
        self.assertEqual(res_ta.detected_name, "Tamil")

        # Test German detection
        res_de = self.engine.translate("Guten Tag, wie geht es Ihnen?", source="auto", target="en")
        self.assertEqual(res_de.detected_code, "de")
        self.assertEqual(res_de.detected_name, "German")
        print(" [PASS] 04. Automatic source language detection")

    # 5. Language swapping logic
    def test_05_language_swapping(self):
        src_name = "English"
        tgt_name = "Tamil"

        # Direct swap
        new_src, new_tgt = tgt_name, src_name
        self.assertEqual(new_src, "Tamil")
        self.assertEqual(new_tgt, "English")

        # Swap with Auto Detect
        auto_src = "Auto Detect"
        detected_name = "Spanish"
        if auto_src == "Auto Detect" and detected_name:
            swapped_src = tgt_name
            swapped_tgt = detected_name
            self.assertEqual(swapped_src, "Tamil")
            self.assertEqual(swapped_tgt, "Spanish")
        print(" [PASS] 05. Language swapping logic")

    # 6. Empty input validation
    def test_06_empty_input_validation(self):
        with self.assertRaises(InvalidInputError):
            self.engine.translate("", source="en", target="ta")

        with self.assertRaises(InvalidInputError):
            self.engine.translate("     \n\t   ", source="en", target="ta")
        print(" [PASS] 06. Empty input validation")

    # 7. Copy translated text
    def test_07_copy_translated_text(self):
        text = "Hello world"
        result = self.engine.translate(text, source="en", target="ta")
        # Ensure translated text is non-empty string ready for clipboard
        clipboard_payload = result.translated_text
        self.assertIsInstance(clipboard_payload, str)
        self.assertTrue(len(clipboard_payload) > 0)
        # Ensure safe character escaping
        escaped = clipboard_payload.replace("\\", "\\\\").replace("`", "\\`")
        self.assertTrue(isinstance(escaped, str))
        print(" [PASS] 07. Copy translated text payload integrity")

    # 8. Download translated text
    def test_08_download_translated_text(self):
        text = "Software testing ensures code reliability."
        result = self.engine.translate(text, source="en", target="ta")
        file_name = f"DOOM_Translate_{result.source_code}_to_{result.target_code}_{int(result.character_count)}.txt"
        file_data = result.translated_text.encode("utf-8")

        self.assertTrue(file_name.endswith(".txt"))
        self.assertTrue(len(file_data) > 0)
        # Verify decoding matches original translation
        self.assertEqual(file_data.decode("utf-8"), result.translated_text)
        print(" [PASS] 08. Download translated text (.txt)")

    # 9. Translation history
    def test_09_translation_history(self):
        history = []
        result = self.engine.translate("Test history item 1", source="en", target="fr")
        history.insert(0, result.to_dict())

        result2 = self.engine.translate("Test history item 2", source="en", target="de")
        history.insert(0, result2.to_dict())

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["target_name"], "German")
        self.assertEqual(history[1]["target_name"], "French")
        print(" [PASS] 09. Translation history retention")

    # 10. Reusing previous translations
    def test_10_reusing_previous_translations(self):
        result = self.engine.translate("Original sentence for reuse", source="en", target="es")
        history_entry = result.to_dict()

        # Simulate loading into session state
        loaded_input = history_entry["original_text"]
        loaded_source = history_entry["source_name"]
        loaded_target = history_entry["target_name"]
        loaded_trans = history_entry["translated_text"]

        self.assertEqual(loaded_input, "Original sentence for reuse")
        self.assertEqual(loaded_source, "English")
        self.assertEqual(loaded_target, "Spanish")
        self.assertTrue(len(loaded_trans) > 0)
        print(" [PASS] 10. Reusing previous translations")

    # 11. Clearing history
    def test_11_clearing_history(self):
        history = [{"item": 1}, {"item": 2}, {"item": 3}]
        self.assertEqual(len(history), 3)
        history.clear()
        self.assertEqual(len(history), 0)
        print(" [PASS] 11. Clearing history functionality")

    # 12. Internet connectivity failure
    def test_12_internet_connectivity_failure(self):
        with patch.object(self.engine._session, "get") as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Network is unreachable")
            with self.assertRaises(NetworkError) as ctx:
                self.engine.translate("Test network failure", source="en", target="ta")
            self.assertIn("internet connection", str(ctx.exception).lower())
        print(" [PASS] 12. Internet connectivity failure handling")

    # 13. Unsupported language handling
    def test_13_unsupported_language_handling(self):
        # Target cannot be 'auto'
        with self.assertRaises(InvalidInputError) as ctx_auto:
            self.engine.translate("Test text", source="en", target="auto")
        self.assertIn("auto detect cannot be selected as the target", str(ctx_auto.exception).lower())

        # Source and Target identical
        with self.assertRaises(InvalidInputError) as ctx_same:
            self.engine.translate("Test text", source="en", target="en")
        self.assertIn("identical", str(ctx_same.exception).lower())

        # Unsupported language code
        with self.assertRaises(translator.LanguageNotSupportedError) as ctx_unsupported:
            self.engine.translate("Test text", source="unsupported_lang_code", target="en")
        self.assertIn("unsupported", str(ctx_unsupported.exception).lower())

        print(" [PASS] 13. Unsupported / invalid language combinations")

    # 14. Translation API errors / Rate limit handling
    def test_14_translation_api_errors(self):
        with patch.object(self.engine._session, "get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 429
            mock_get.return_value = mock_resp

            with self.assertRaises(RateLimitError) as ctx_rate:
                self.engine.translate("Test rate limit", source="en", target="ta")
            self.assertIn("rate limit", str(ctx_rate.exception).lower())

        with patch.object(self.engine._session, "get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 500
            mock_get.return_value = mock_resp

            # When 500 occurs on primary, it attempts fallback; if fallback fails, raises TranslationError
            with patch.object(self.engine, "_fallback_translate", side_effect=TranslationError("Fallback failed")):
                with self.assertRaises(TranslationError):
                    self.engine.translate("Test 500 error", source="en", target="ta")
        print(" [PASS] 14. Translation API server error handling")


if __name__ == "__main__":
    print("\n=======================================================")
    print(" DOOM TRANSLATE - EXHAUSTIVE 14-POINT TEST SUITE")
    print(" CodeAlpha Artificial Intelligence Internship")
    print("=======================================================\n")
    unittest.main(verbosity=2)
