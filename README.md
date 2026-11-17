# DOOM Translate – AI Language Translation Tool 🌐⚡

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%20%7C%203.12-00C878?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-39FF88?style=for-the-badge&logo=streamlit&logoColor=061A12)](https://streamlit.io/)
[![Deep Translator](https://img.shields.io/badge/Engine-Google%20Neural%20API-00C878?style=for-the-badge&logo=google-translate&logoColor=white)](https://translate.google.com/)
[![License](https://img.shields.io/badge/License-MIT-0B2419?style=for-the-badge)](LICENSE)
[![Internship](https://img.shields.io/badge/Internship-CodeAlpha%20AI-00C878?style=for-the-badge)](https://www.codealpha.tech/)

> **Tagline:** BREAK LANGUAGE BARRIERS.  
> **Application Name:** DOOM Translate  
> **Internship:** CodeAlpha Artificial Intelligence Internship  
> **GitHub Repository:** `CodeAlpha_DOOMTranslate`  
> **Theme:** Dark Forest Green & Emerald AI SaaS Interface (`#061A12` / `#00C878`)

---

## 📌 1. Project Overview & Objectives

**DOOM Translate** is an AI-powered language translation application engineered using Python and Streamlit. Developed as part of the **CodeAlpha Artificial Intelligence Internship**, the application enables frictionless multilingual communication across **133 world languages and regional dialects** through a real-time neural translation pipeline.

Unlike static mockups or superficial demonstrations, DOOM Translate communicates dynamically with production-grade neural machine translation backends. The platform features intelligent language auto-detection, resilient error handling, long-text paragraph chunking, live connection diagnostics, and interactive session history.

### Core Objectives
1. **Accurate Neural Translation:** Transmit real user queries to neural translation backends and return accurate, context-aware translations.
2. **Comprehensive Linguistic Diversity:** Provide full bi-directional support for Indian languages (Tamil, Hindi, Telugu, Malayalam, Kannada, Bengali, etc.) and major international languages (French, German, Spanish, Japanese, Chinese, Arabic, Russian, etc.).
3. **Automatic Language Detection:** Recognize source languages automatically without requiring manual language configuration.
4. **Resilient Multi-Tier Architecture:** Built with an intelligent failover pipeline, network timeout safeguards, and rate-limit mitigation.
5. **Premium AI SaaS UI/UX:** Designed with an emerald green glow and dark forest green glassmorphism aesthetic inspired by modern AI productivity suites.

---

## ✨ 2. Key Features

| Category | Feature Description |
| :--- | :--- |
| **Source Text Input** | Large multiline text input area with live character counter, word counter, and one-click clear button. |
| **Language Selection** | Source selector with *Auto Detect* plus 133 supported languages; target dropdown with instant filtering. |
| **Quick Selection Pills** | One-click language badges for high-frequency languages (English, Tamil, Hindi, Telugu, French, Spanish, etc.). |
| **Smart Language Swap** | `⇄` swap button that dynamically switches source and destination languages and exchanges input/output text. |
| **Real-Time Translation Engine** | Neural translation powered by Google Neural Translation API with Deep-Translator fallbacks. |
| **Output Workspace** | Distinct emerald output card displaying translated results, detected source badge, and engine metrics. |
| **One-Click Clipboard Copy** | Instant JavaScript-powered clipboard copy with visual toast notifications. |
| **Plain Text File Export** | Download translations as clean `.txt` files with automated nomenclature. |
| **Session Translation History** | In-memory session tracking showing previous translations, timestamps, word metrics, and reusable prompts. |
| **Privacy Compliance** | Zero permanent storage of sensitive user text; all data resides strictly in volatile session memory. |
| **Live Connection Diagnostics** | Latency telemetry and live backend health indicator directly in the top navigation bar. |

---

## 🎨 3. UI/UX Design System & Theme

DOOM Translate features an exclusive **Dark Forest Green + Emerald Green** palette tailored for modern AI SaaS applications:

```
┌────────────────────────────────────────────────────────┐
│               DOOM TRANSLATE COLOR PALETTE             │
├────────────────────────────────┬───────────────────────┤
│ Element                        │ Color Hex             │
├────────────────────────────────┼───────────────────────┤
│ Main Background                │ #061A12               │
│ Secondary Background           │ #0B2419               │
│ Card / Panel Background        │ #102F21 (Glassmorphic)│
│ Primary Accent                 │ #00C878 (Emerald)     │
│ Secondary Accent               │ #39FF88 (Neon Glow)   │
│ Main Text                      │ #F5FFF8               │
│ Secondary Text                 │ #A7C9B5               │
│ Border & Dividers              │ #1B4933               │
└────────────────────────────────┴───────────────────────┘
```

- **Visual Effects:** 14px rounded corners, glassmorphism blur (`backdrop-filter: blur(12px)`), neon green glowing hover states, and smooth CSS transitions.
- **Responsive Layout:** Adaptive two-panel translation view optimized for widescreen monitors, laptops, and mobile screens.

---

## 🏗️ 4. Project Structure

```
DOOM_Translate/
│
├── .streamlit/
│   └── config.toml           # Streamlit theme and server configuration
│
├── assets/
│   └── logo.png              # High-resolution futuristic emerald app logo
│
├── app.py                    # Main Streamlit UI, interaction logic, and state management
├── translator.py             # Translation engine, multi-tier fallback, and error recovery
├── language_data.py          # 133+ language definitions, ISO codes, flags, and categories
├── test_doom_translate.py    # Automated 14-point internship compliance test suite
│
├── requirements.txt          # Python project dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git exclusions (venv, secrets, cache)
└── README.md                 # Complete project documentation
```

### File Responsibilities
- **`app.py`:** Manages page layout, custom CSS styling, tab navigation, input bindings, clipboard interactions, and session state.
- **`translator.py`:** Contains the `DOOMTranslator` class. Decouples translation requests from UI components, executes text chunking for long inputs, detects languages, and raises typed exceptions (`NetworkError`, `RateLimitError`, `InvalidInputError`).
- **`language_data.py`:** Provides an indexed catalog of 133 languages, country flag emojis, ISO 639-1 mappings, and regional groupings.
- **`test_doom_translate.py`:** Standalone test suite executing the 14 mandatory validation scenarios.

---

## ⚙️ 5. Technology Stack

- **Core Runtime:** Python 3.11+ / Python 3.12
- **Web Framework:** [Streamlit](https://streamlit.io/) (1.35+)
- **Translation Services:**
  - Google Neural Machine Translation API (Primary Engine)
  - `deep-translator` (Failover Architecture)
- **HTTP Client:** `requests` (with session pooling and latency telemetry)
- **Image Processing:** `Pillow` (Pillow 10+)
- **Environment Management:** `python-dotenv`

---

## 🚀 6. Installation & Setup Guide (Windows)

Follow these exact commands in your Windows terminal (`PowerShell` or `Command Prompt`):

### Step 1: Clone or Open the Repository
```powershell
cd C:\Users\<YourUsername>\Desktop
git clone https://github.com/<YourUsername>/CodeAlpha_DOOMTranslate.git DOOM_Translate
cd DOOM_Translate
```

### Step 2: Create a Python Virtual Environment
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
- **PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If execution policies restrict scripts, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*
- **Command Prompt (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: (Optional) Configure Environment Variables
```powershell
copy .env.example .env
```

---

## 🖥️ 7. Running the Application

Execute the following command from the root `DOOM_Translate` directory:

```powershell
streamlit run app.py
```

Upon launch, Streamlit will display the local server address:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in your web browser to interact with DOOM Translate.

---

## 🧪 8. Testing & Validation Suite

DOOM Translate includes an automated, self-contained test suite in `test_doom_translate.py`. To execute all 14 required verification scenarios:

```powershell
python test_doom_translate.py
```

### Test Case Verification Matrix

| # | Test Case Scenario | Validation Method | Result |
| :-: | :--- | :--- | :-: |
| **01** | English to Tamil Translation | Verified Unicode range `\u0B80-\u0BFF` and accurate vocabulary | **PASS** ✅ |
| **02** | English to Hindi Translation | Verified Devanagari Unicode `\u0900-\u097F` and semantic accuracy | **PASS** ✅ |
| **03** | Tamil to English Translation | Verified reverse translation of `வணக்கம் உலகம்` | **PASS** ✅ |
| **04** | Automatic Source Language Detection | Evaluated auto-detection on French (`fr`), Tamil (`ta`), and German (`de`) | **PASS** ✅ |
| **05** | Language Swapping Logic | Verified bidirectional parameter inversion and Auto-Detect resolution | **PASS** ✅ |
| **06** | Empty Input Validation | Ensured `InvalidInputError` is raised for empty/whitespace input | **PASS** ✅ |
| **07** | Copy Translated Text Payload | Validated string escaping and clipboard payload integrity | **PASS** ✅ |
| **08** | Download Translated Text (.txt) | Verified UTF-8 plain-text encoding and formatted file naming | **PASS** ✅ |
| **09** | Translation History Retention | Verified FIFO session state list and metadata accuracy | **PASS** ✅ |
| **10** | Reusing Previous Translations | Verified loading historical prompts back into the active editor | **PASS** ✅ |
| **11** | Clearing History Functionality | Verified atomic memory cleanup on session history reset | **PASS** ✅ |
| **12** | Internet Connectivity Failure | Mocked network socket disconnect; verified graceful `NetworkError` | **PASS** ✅ |
| **13** | Unsupported / Invalid Languages | Verified validation for identical languages and invalid codes | **PASS** ✅ |
| **14** | Translation API / Rate Limit Errors | Mocked HTTP 429 & 500 status codes; verified `RateLimitError` handling | **PASS** ✅ |

---

## 🛡️ 9. Privacy, Security & Data Handling

- **Zero Permanent Storage:** DOOM Translate does not log or persist translated text to databases, disk, or remote analytics platforms.
- **Volatile Session Memory:** User history exists strictly within the ephemeral `st.session_state` of the current browser session. Refreshing or terminating the browser completely clears the history.
- **Secure Network Tunnels:** All external translation payloads are transmitted over encrypted TLS/HTTPS endpoints.

---

## ⚠️ 10. Known Limitations & Future Enhancements

### Known Limitations
- High-volume rapid requests from a single IP may trigger temporary Google rate limits (handled gracefully via the fallback engine).
- Formatting within complex tables or markdown code blocks may occasionally be normalized as plain text.

### Future Enhancements
- [ ] Integration with offline LLM engines (e.g., Llama.cpp / Ollama) for zero-internet translation.
- [ ] Document translation support (PDF, DOCX, and CSV batch processing).
- [ ] Custom user vocabulary glossaries for domain-specific medical and legal terms.

---

## 💼 11. CodeAlpha Internship Submission Details

- **Internship Program:** CodeAlpha Artificial Intelligence Internship
- **Task Assigned:** Language Translation Tool
- **Developer:** M. Keerthaesh
- **Submission Date:** November 2026
- **Compliance Status:** 100% compliant with internship specifications (complete application, modular architecture, real translation engine, professional UI/UX, and comprehensive documentation).

---

## 📤 12. Publishing to GitHub

To push your repository to GitHub:

```powershell
git init
git add .
git commit -m "feat: complete DOOM Translate AI translation tool for CodeAlpha internship"
git branch -M main
git remote add origin https://github.com/<YourUsername>/CodeAlpha_DOOMTranslate.git
git push -u origin main
```

---

<p align="center">
  <b>DOOM Translate &bull; BREAK LANGUAGE BARRIERS</b><br>
  Developed with ❤️ for the CodeAlpha Artificial Intelligence Internship
</p>
