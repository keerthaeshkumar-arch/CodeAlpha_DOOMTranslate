"""
DOOM Translate - Language Data Module
Defines supported language names, codes, flag mappings, and categorical classifications.
Developed for CodeAlpha Artificial Intelligence Internship.
"""

from typing import Dict, List, Optional, Tuple

AUTO_DETECT_CODE = "auto"
AUTO_DETECT_NAME = "Auto Detect"

# Key popular languages highlighted in quick selection & top dropdowns
POPULAR_LANGUAGES: Dict[str, str] = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Malayalam": "ml",
    "Kannada": "kn",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Arabic": "ar",
    "Korean": "ko",
    "Portuguese": "pt",
    "Russian": "ru",
    "Italian": "it",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
}

# Flag / regional emoji mapping for enhanced visual aesthetics
LANGUAGE_FLAGS: Dict[str, str] = {
    "auto": "✨",
    "en": "🇬🇧",
    "ta": "🇮🇳",
    "hi": "🇮🇳",
    "te": "🇮🇳",
    "ml": "🇮🇳",
    "kn": "🇮🇳",
    "bn": "🇧🇩",
    "mr": "🇮🇳",
    "gu": "🇮🇳",
    "pa": "🇮🇳",
    "ur": "🇵🇰",
    "fr": "🇫🇷",
    "de": "🇩🇪",
    "es": "🇪🇸",
    "ja": "🇯🇵",
    "zh-CN": "🇨🇳",
    "zh-TW": "🇹🇼",
    "ar": "🇸🇦",
    "ko": "🇰🇷",
    "pt": "🇵🇹",
    "ru": "🇷🇺",
    "it": "🇮🇹",
    "nl": "🇳🇱",
    "tr": "🇹🇷",
    "vi": "🇻🇳",
    "th": "🇹🇭",
    "id": "🇮🇩",
    "pl": "🇵🇱",
    "uk": "🇺🇦",
    "sv": "🇸🇪",
    "el": "🇬🇷",
    "cs": "🇨🇿",
    "ro": "🇷🇴",
    "hu": "🇭🇺",
    "da": "🇩🇰",
    "fi": "🇫🇮",
    "no": "🇳🇴",
    "he": "🇮🇱",
    "fa": "🇮🇷",
    "ms": "🇲🇾",
    "fil": "🇵🇭",
    "sw": "🇰🇪",
    "ne": "🇳🇵",
    "si": "🇱🇰",
}

# Comprehensive master list of all 133 supported Google Translate languages
ALL_LANGUAGES: Dict[str, str] = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Aymara": "ay",
    "Azerbaijani": "az",
    "Bambara": "bm",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bhojpuri": "bho",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chichewa": "ny",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dhivehi": "dv",
    "Dogri": "doi",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Ewe": "ee",
    "Filipino (Tagalog)": "fil",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Guarani": "gn",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Ilocano": "ilo",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Konkani": "gom",
    "Korean": "ko",
    "Krio": "kri",
    "Kurdish (Kurmanji)": "ku",
    "Kurdish (Sorani)": "ckb",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Luganda": "lg",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Maithili": "mai",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Meiteilon (Manipuri)": "mni-Mtei",
    "Mizo": "lus",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Odia (Oriya)": "or",
    "Oromo": "om",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Quechua": "qu",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Sanskrit": "sa",
    "Scots Gaelic": "gd",
    "Sepedi": "nso",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Tigrinya": "ti",
    "Tsonga": "ts",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Twi": "ak",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}

# Reverse mapping: code -> Display Name
CODE_TO_NAME: Dict[str, str] = {code: name for name, code in ALL_LANGUAGES.items()}
CODE_TO_NAME[AUTO_DETECT_CODE] = AUTO_DETECT_NAME
# Additional aliases for detected language codes
CODE_TO_NAME["zh"] = "Chinese (Simplified)"
CODE_TO_NAME["zh-cn"] = "Chinese (Simplified)"
CODE_TO_NAME["zh-tw"] = "Chinese (Traditional)"
CODE_TO_NAME["iw"] = "Hebrew"
CODE_TO_NAME["jw"] = "Javanese"

# Regional Categories for the Supported Languages explorer
LANGUAGE_REGIONS: Dict[str, List[str]] = {
    "Indian Languages": [
        "Tamil", "Hindi", "Telugu", "Malayalam", "Kannada", "Bengali",
        "Marathi", "Gujarati", "Punjabi", "Urdu", "Assamese", "Bhojpuri",
        "Dogri", "Konkani", "Maithili", "Meiteilon (Manipuri)", "Mizo",
        "Odia (Oriya)", "Sanskrit", "Sindhi"
    ],
    "European Languages": [
        "English", "French", "German", "Spanish", "Portuguese", "Italian",
        "Russian", "Dutch", "Polish", "Ukrainian", "Swedish", "Greek",
        "Czech", "Romanian", "Hungarian", "Danish", "Finnish", "Norwegian",
        "Bulgarian", "Croatian", "Serbian", "Slovak", "Irish", "Latin"
    ],
    "Asian Languages": [
        "Japanese", "Chinese (Simplified)", "Chinese (Traditional)", "Korean",
        "Vietnamese", "Thai", "Indonesian", "Malay", "Filipino (Tagalog)",
        "Myanmar (Burmese)", "Khmer", "Lao", "Mongolian", "Nepali", "Sinhala"
    ],
    "Middle Eastern & African": [
        "Arabic", "Persian", "Hebrew", "Turkish", "Swahili", "Amharic",
        "Hausa", "Yoruba", "Igbo", "Zulu", "Somali", "Kurdish (Kurmanji)",
        "Pashto", "Afrikaans"
    ]
}


def get_source_language_options() -> List[str]:
    """Returns sorted display names for source language dropdown with Auto Detect first."""
    options = [AUTO_DETECT_NAME]
    sorted_langs = sorted(ALL_LANGUAGES.keys())
    options.extend(sorted_langs)
    return options


def get_target_language_options() -> List[str]:
    """Returns sorted display names for target language dropdown (excluding Auto Detect)."""
    return sorted(ALL_LANGUAGES.keys())


def get_code_by_name(name: str) -> str:
    """Returns the ISO language code for a given display name."""
    if name == AUTO_DETECT_NAME:
        return AUTO_DETECT_CODE
    return ALL_LANGUAGES.get(name, "en")


def get_name_by_code(code: str) -> str:
    """Returns the display name for a given language code."""
    cleaned = code.strip().lower()
    for c, n in CODE_TO_NAME.items():
        if c.lower() == cleaned:
            return n
    return code.upper()


def get_language_flag(code_or_name: str) -> str:
    """Returns the flag emoji for a language code or name."""
    if code_or_name in ALL_LANGUAGES:
        code = ALL_LANGUAGES[code_or_name]
    else:
        code = code_or_name
    return LANGUAGE_FLAGS.get(code.lower(), LANGUAGE_FLAGS.get(code, "🌐"))


def is_valid_code(code: str) -> bool:
    """Checks whether a language code is supported."""
    cleaned = code.strip().lower()
    return any(c.lower() == cleaned for c in CODE_TO_NAME.keys())


def format_language_label(name: str) -> str:
    """Formats language with flag emoji for UI display."""
    code = get_code_by_name(name)
    flag = get_language_flag(code)
    return f"{flag} {name}"
