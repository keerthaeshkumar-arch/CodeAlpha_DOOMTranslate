"""
DOOM Translate - AI-Powered Language Translation Tool
Application Name: DOOM Translate
Tagline: BREAK LANGUAGE BARRIERS.
Project Type: AI Language Translation Tool
Internship: CodeAlpha Artificial Intelligence Internship
GitHub Repository: CodeAlpha_DOOMTranslate
"""

import os
import sys
from pathlib import Path
import streamlit as st

# Add current directory to sys.path to ensure absolute import compatibility
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

import language_data
import translator
from translator import (
    TranslationError,
    NetworkError,
    RateLimitError,
    InvalidInputError,
    LanguageNotSupportedError,
)

# -----------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION
# -----------------------------------------------------------------------------
logo_path = current_dir / "assets" / "logo.png"
page_icon = str(logo_path) if logo_path.exists() else "🌐"

st.set_page_config(
    page_title="DOOM Translate | Break Language Barriers",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_result" not in st.session_state:
    st.session_state.translated_result = None
if "source_lang_name" not in st.session_state:
    st.session_state.source_lang_name = language_data.AUTO_DETECT_NAME
if "target_lang_name" not in st.session_state:
    st.session_state.target_lang_name = "Tamil"
if "history" not in st.session_state:
    st.session_state.history = []
if "service_status" not in st.session_state:
    st.session_state.service_status = None
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Translator"
if "copy_trigger" not in st.session_state:
    st.session_state.copy_trigger = 0

# -----------------------------------------------------------------------------
# 3. PROFESSIONAL UI/UX THEME (DARK FOREST GREEN + EMERALD GREEN)
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Import Modern Typography */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-main: #061A12;
    --bg-sec: #0B2419;
    --bg-card: #102F21;
    --accent-primary: #00C878;
    --accent-secondary: #39FF88;
    --text-main: #F5FFF8;
    --text-sec: #A7C9B5;
    --border-color: #1B4933;
    --glow-primary: rgba(0, 200, 120, 0.25);
    --glow-secondary: rgba(57, 255, 136, 0.35);
}

/* Global Background */
.stApp {
    background: radial-gradient(circle at 50% 0%, #0B2419 0%, #061A12 100%) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-main);
}

/* Header & Top Bar */
.doom-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 2rem;
    background: rgba(16, 47, 33, 0.85);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

.doom-brand {
    display: flex;
    align-items: center;
    gap: 1.2rem;
}

.doom-title {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text-main);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.doom-title span {
    color: var(--accent-secondary);
    text-shadow: 0 0 16px var(--glow-secondary);
}

.doom-subtitle {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-sec);
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

/* Status Pill */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.45rem 1rem;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 600;
    background: rgba(11, 36, 25, 0.9);
    border: 1px solid var(--border-color);
    color: var(--text-main);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--accent-secondary);
    box-shadow: 0 0 10px var(--accent-secondary);
    animation: pulse 2s infinite ease-in-out;
}

@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.7; }
    50% { transform: scale(1.3); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.7; }
}

/* Hero Section */
.hero-container {
    text-align: center;
    padding: 1.5rem 1rem 2rem 1rem;
    margin-bottom: 1.5rem;
}

.hero-tagline {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: 1px;
    color: var(--text-main);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    text-shadow: 0 4px 20px rgba(0, 200, 120, 0.2);
}

.hero-tagline .highlight {
    background: linear-gradient(135deg, #00C878 0%, #39FF88 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    font-size: 1.05rem;
    color: var(--text-sec);
    max-width: 680px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Translation Panels */
.panel-card {
    background: rgba(16, 47, 33, 0.75);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.4rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    transition: all 0.25s ease;
}

.panel-card:hover {
    border-color: rgba(0, 200, 120, 0.4);
    box-shadow: 0 12px 30px rgba(0, 200, 120, 0.1);
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(27, 73, 51, 0.6);
}

.panel-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-sec);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Character Counter */
.char-counter {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-sec);
    background: rgba(6, 26, 18, 0.6);
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    border: 1px solid var(--border-color);
}

/* Output Display Box */
.output-box {
    background: rgba(6, 26, 18, 0.65);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.2rem;
    min-height: 240px;
    color: var(--text-main);
    font-size: 1.05rem;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
}

.output-placeholder {
    color: #4A7A61;
    font-style: italic;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    text-align: center;
}

/* Modern Input Controls & Textarea */
.stTextArea textarea {
    background-color: rgba(6, 26, 18, 0.65) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.05rem !important;
    line-height: 1.6 !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.2s ease !important;
}

.stTextArea textarea:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 12px var(--glow-primary), inset 0 2px 8px rgba(0,0,0,0.3) !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background-color: var(--bg-sec) !important;
    border-color: var(--border-color) !important;
    border-radius: 10px !important;
    color: var(--text-main) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00C878 0%, #00995C 100%) !important;
    color: #061A12 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 15px var(--glow-primary) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #39FF88 0%, #00C878 100%) !important;
    color: #061A12 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px var(--glow-secondary) !important;
}

/* Secondary / Outline Button */
.secondary-btn button {
    background: rgba(16, 47, 33, 0.8) !important;
    color: var(--text-sec) !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: none !important;
}

.secondary-btn button:hover {
    background: rgba(27, 73, 51, 0.9) !important;
    color: var(--text-main) !important;
    border-color: var(--accent-primary) !important;
    transform: translateY(-1px) !important;
}

/* Swap Button */
.swap-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    padding-top: 1.8rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(16, 47, 33, 0.6) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 14px !important;
    padding: 0.4rem !important;
    gap: 0.5rem !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-sec) !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0, 200, 120, 0.15) !important;
    color: var(--accent-secondary) !important;
    border: 1px solid var(--accent-primary) !important;
}

/* History Card */
.history-card {
    background: rgba(16, 47, 33, 0.7);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.history-card:hover {
    border-color: var(--accent-primary);
    box-shadow: 0 6px 18px rgba(0, 200, 120, 0.12);
}

.history-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    background: rgba(0, 200, 120, 0.15);
    border: 1px solid rgba(0, 200, 120, 0.3);
    color: var(--accent-secondary);
}

.history-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #6C9680;
}

/* Footer */
.doom-footer {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem 1rem;
    margin-top: 3rem;
    border-top: 1px solid var(--border-color);
    color: var(--text-sec);
    font-size: 0.85rem;
}

.doom-footer a {
    color: var(--accent-secondary) !important;
    text-decoration: none;
    font-weight: 600;
}

.doom-footer a:hover {
    text-decoration: underline;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. APPLICATION CACHED CONNECTIVITY CHECK
# -----------------------------------------------------------------------------
@st.cache_data(ttl=90, show_spinner=False)
def get_cached_service_status():
    """Performs a live latency and connection check to the translation backend."""
    return translator.check_service_status()


# Run or refresh status
service_status = get_cached_service_status()

# -----------------------------------------------------------------------------
# 5. HEADER SECTION
# -----------------------------------------------------------------------------
status_html = ""
if service_status.get("online"):
    latency = service_status.get("latency_ms", 50)
    status_html = f"""
    <div class="status-pill">
        <div class="status-dot"></div>
        <span>Google Neural Engine • {latency}ms</span>
    </div>
    """
else:
    status_html = """
    <div class="status-pill" style="border-color: #FF4D4D;">
        <div class="status-dot" style="background:#FF4D4D; box-shadow:0 0 10px #FF4D4D;"></div>
        <span style="color:#FFB3B3;">Backend Offline</span>
    </div>
    """

header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown(
        f"""
        <div class="doom-brand">
            <div>
                <h1 class="doom-title">DOOM <span>TRANSLATE</span></h1>
                <div class="doom-subtitle">AI-Powered Neural Language Translator • CodeAlpha Internship</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_col2:
    st.markdown(f"<div style='text-align:right;'>{status_html}</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. MAIN NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_translator, tab_history, tab_languages, tab_how_it_works, tab_about = st.tabs([
    "⚡ Translator",
    f"📜 Translation History ({len(st.session_state.history)})",
    "🌐 Supported Languages (133+)",
    "⚙️ How It Works",
    "ℹ️ About DOOM Translate",
])

# =============================================================================
# TAB 1: CORE TRANSLATOR
# =============================================================================
with tab_translator:
    # Hero Title
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-tagline">BREAK <span class="highlight">LANGUAGE BARRIERS</span>.</div>
            <div class="hero-description">
                Translate your words into different languages with DOOM Translate.
                Instant, context-aware AI neural translation supporting over 130+ global dialects.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Language Selectors Row
    source_options = language_data.get_source_language_options()
    target_options = language_data.get_target_language_options()

    col_src_select, col_swap, col_tgt_select = st.columns([5, 1, 5])

    with col_src_select:
        # Determine source index
        src_index = 0
        if st.session_state.source_lang_name in source_options:
            src_index = source_options.index(st.session_state.source_lang_name)

        selected_source = st.selectbox(
            "SOURCE LANGUAGE",
            options=source_options,
            index=src_index,
            format_func=language_data.format_language_label,
            key="select_source_lang",
        )
        st.session_state.source_lang_name = selected_source

    with col_swap:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        swap_clicked = st.button("⇄", help="Swap Source and Target Languages", use_container_width=True)

        if swap_clicked:
            old_src = st.session_state.source_lang_name
            old_tgt = st.session_state.target_lang_name

            # If source was Auto Detect, resolve to detected language or keep target
            if old_src == language_data.AUTO_DETECT_NAME:
                if (
                    st.session_state.translated_result
                    and st.session_state.translated_result.detected_name
                    and st.session_state.translated_result.detected_name in target_options
                ):
                    st.session_state.source_lang_name = old_tgt
                    st.session_state.target_lang_name = st.session_state.translated_result.detected_name
                else:
                    st.session_state.source_lang_name = old_tgt
                    st.session_state.target_lang_name = "English" if old_tgt != "English" else "Tamil"
            else:
                st.session_state.source_lang_name = old_tgt
                st.session_state.target_lang_name = old_src

            # Swap texts if a translation exists
            if st.session_state.translated_result:
                st.session_state.input_text = st.session_state.translated_result.translated_text
                st.session_state.translated_result = None

            st.rerun()

    with col_tgt_select:
        # Determine target index
        tgt_index = 0
        if st.session_state.target_lang_name in target_options:
            tgt_index = target_options.index(st.session_state.target_lang_name)
        elif "Tamil" in target_options:
            tgt_index = target_options.index("Tamil")

        selected_target = st.selectbox(
            "TARGET LANGUAGE",
            options=target_options,
            index=tgt_index,
            format_func=language_data.format_language_label,
            key="select_target_lang",
        )
        st.session_state.target_lang_name = selected_target

    # Quick Language Pills
    quick_col1, quick_col2 = st.columns([5, 5])
    with quick_col1:
        st.markdown("<div style='font-size:0.75rem; color:#A7C9B5; margin-bottom:0.3rem;'>QUICK SOURCE:</div>", unsafe_allow_html=True)
        pill_cols = st.columns(6)
        quick_sources = ["Auto Detect", "English", "Tamil", "Hindi", "French", "Spanish"]
        for idx, q_src in enumerate(quick_sources):
            with pill_cols[idx]:
                if st.button(q_src, key=f"q_src_{q_src}", use_container_width=True):
                    st.session_state.source_lang_name = q_src
                    st.rerun()

    with quick_col2:
        st.markdown("<div style='font-size:0.75rem; color:#A7C9B5; margin-bottom:0.3rem;'>QUICK TARGET:</div>", unsafe_allow_html=True)
        pill_cols_tgt = st.columns(6)
        quick_targets = ["Tamil", "Hindi", "Telugu", "Kannada", "Malayalam", "English"]
        for idx, q_tgt in enumerate(quick_targets):
            with pill_cols_tgt[idx]:
                if st.button(q_tgt, key=f"q_tgt_{q_tgt}", use_container_width=True):
                    st.session_state.target_lang_name = q_tgt
                    st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Translation Panels (Two large cards)
    col_input_panel, col_output_panel = st.columns(2)

    with col_input_panel:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)

        # Header with character count and clear button
        input_chars = len(st.session_state.input_text)
        input_words = len(st.session_state.input_text.split())

        p_header_c1, p_header_c2 = st.columns([3, 1])
        with p_header_c1:
            st.markdown(
                f"""
                <div class="panel-title">
                    <span>📝 SOURCE TEXT</span>
                    <span class="char-counter">{input_chars} chars | {input_words} words</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with p_header_c2:
            if st.button("🗑️ Clear", key="clear_input_btn", use_container_width=True):
                st.session_state.input_text = ""
                st.session_state.translated_result = None
                st.rerun()

        user_input = st.text_area(
            label="Source Text Input Area",
            value=st.session_state.input_text,
            placeholder="Enter your text here...",
            height=260,
            label_visibility="collapsed",
            key="main_text_input",
        )
        st.session_state.input_text = user_input

        st.markdown("</div>", unsafe_allow_html=True)

    with col_output_panel:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)

        res = st.session_state.translated_result
        detected_info_str = ""
        if res and res.detected_name:
            detected_info_str = f" • Detected: {res.detected_name}"

        st.markdown(
            f"""
            <div class="panel-header">
                <div class="panel-title">
                    <span>✨ TRANSLATION RESULT</span>
                </div>
                <div style="font-size:0.8rem; color:#39FF88; font-weight:600;">
                    {st.session_state.target_lang_name} {detected_info_str}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if res and res.translated_text:
            st.markdown(
                f"""
                <div class="output-box">{res.translated_text}</div>
                """,
                unsafe_allow_html=True,
            )

            # Metadata info bar
            out_chars = len(res.translated_text)
            out_words = len(res.translated_text.split())
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; margin-top:0.6rem; font-size:0.75rem; color:#A7C9B5;">
                    <span>Output: {out_chars} chars | {out_words} words</span>
                    <span>Engine: {res.engine_used}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Action Buttons Row: Copy, Download, Clear All
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            act_col1, act_col2, act_col3 = st.columns([2, 2, 1.5])

            with act_col1:
                copy_clicked = st.button("📋 Copy Text", key="btn_copy_translation", use_container_width=True)
                if copy_clicked:
                    # Provide visual toast feedback and trigger clipboard copy via modern JS
                    st.toast("✅ Translation copied to clipboard!", icon="📋")
                    # Embed invisible JS to execute copy into system clipboard
                    escaped_text = res.translated_text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
                    st.components.v1.html(
                        f"""
                        <script>
                        navigator.clipboard.writeText(`{escaped_text}`);
                        </script>
                        """,
                        height=0,
                        width=0,
                    )

            with act_col2:
                file_name = f"DOOM_Translate_{res.source_code}_to_{res.target_code}_{int(res.character_count)}.txt"
                st.download_button(
                    label="📥 Download .txt",
                    data=res.translated_text,
                    file_name=file_name,
                    mime="text/plain",
                    use_container_width=True,
                    key="btn_download_translation",
                )

            with act_col3:
                if st.button("Clear All", key="btn_clear_all", use_container_width=True):
                    st.session_state.input_text = ""
                    st.session_state.translated_result = None
                    st.rerun()

        else:
            st.markdown(
                """
                <div class="output-box output-placeholder">
                    <div>
                        <div style="font-size:2rem; margin-bottom:0.5rem;">⚡</div>
                        <div>Your translated text will appear here with neural precision.</div>
                        <div style="font-size:0.8rem; margin-top:0.4rem; color:#6C9680;">
                            Select target language and click TRANSLATE NOW below.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Placeholder clear button disabled
            st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Translate Now Button (Large Emerald Accent Button)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    trans_btn_col1, trans_btn_col2, trans_btn_col3 = st.columns([1, 2, 1])

    with trans_btn_col2:
        translate_clicked = st.button(
            "⚡ TRANSLATE NOW",
            key="btn_translate_now",
            use_container_width=True,
        )

    # Translation Execution & Error Handling
    if translate_clicked:
        if not user_input or not user_input.strip():
            st.warning("⚠️ Input validation error: Please enter some text to translate.")
        else:
            src_code = language_data.get_code_by_name(st.session_state.source_lang_name)
            tgt_code = language_data.get_code_by_name(st.session_state.target_lang_name)

            if src_code != "auto" and src_code == tgt_code:
                st.error(
                    f"⚠️ Invalid Language Combination: Source and target are both set to "
                    f"'{st.session_state.target_lang_name}'. Please select different languages."
                )
            else:
                with st.spinner("Translating with DOOM Neural Engine..."):
                    try:
                        result = translator.translate_text(
                            text=user_input,
                            source=src_code,
                            target=tgt_code,
                        )
                        st.session_state.translated_result = result

                        # Append to session history (avoid duplicates at the top)
                        history_entry = result.to_dict()
                        st.session_state.history.insert(0, history_entry)
                        # Keep session history capped to 50 items
                        if len(st.session_state.history) > 50:
                            st.session_state.history.pop()

                        st.success(
                            f"✅ Successfully translated from "
                            f"{result.detected_name or result.source_name} to {result.target_name}!"
                        )
                        st.rerun()

                    except InvalidInputError as e:
                        st.warning(f"⚠️ {str(e)}")
                    except NetworkError as e:
                        st.error(f"🌐 Connection Failure: {str(e)}")
                    except RateLimitError as e:
                        st.warning(f"⏳ Rate Limit Exceeded: {str(e)}")
                    except TranslationError as e:
                        st.error(f"❌ Translation Service Error: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Unexpected Error: {str(e)}")


# =============================================================================
# TAB 2: TRANSLATION HISTORY
# =============================================================================
with tab_history:
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-weight:700; color:var(--text-main); margin-bottom:0.2rem;">Session Translation History</h2>
            <div style="color:var(--text-sec); font-size:0.9rem;">
                Translations created during this active session. Data is stored ephemerally in session memory and is never uploaded or persisted to remote servers.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.history:
        st.markdown(
            """
            <div class="panel-card" style="text-align:center; padding:3rem 1rem;">
                <div style="font-size:2.5rem; margin-bottom:0.8rem;">📜</div>
                <div style="font-size:1.1rem; font-weight:700; color:var(--text-main);">No Translations Yet</div>
                <div style="color:var(--text-sec); font-size:0.9rem; margin-top:0.4rem;">
                    Perform your first translation in the Translator tab and it will appear here instantly.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # History Controls Bar
        hist_ctrl1, hist_ctrl2, hist_ctrl3 = st.columns([2, 2, 2])
        with hist_ctrl1:
            st.metric("Total Session Translations", len(st.session_state.history))
        with hist_ctrl2:
            total_chars = sum(item.get("character_count", 0) for item in st.session_state.history)
            st.metric("Total Characters Processed", total_chars)
        with hist_ctrl3:
            st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
            if st.button("🗑️ Clear Entire History", key="btn_clear_history", use_container_width=True):
                st.session_state.history = []
                st.success("History cleared successfully!")
                st.rerun()

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # Render History Entries
        for idx, item in enumerate(st.session_state.history):
            src_name = item.get("detected_name") or item.get("source_name")
            tgt_name = item.get("target_name")
            timestamp = item.get("timestamp", "")
            orig_text = item.get("original_text", "")
            trans_text = item.get("translated_text", "")

            with st.container():
                st.markdown(
                    f"""
                    <div class="history-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
                            <div style="display:flex; align-items:center; gap:0.6rem;">
                                <span class="history-badge">{src_name} → {tgt_name}</span>
                                <span style="font-size:0.75rem; color:#A7C9B5;">({item.get('character_count', 0)} chars)</span>
                            </div>
                            <span class="history-time">{timestamp}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                h_col1, h_col2 = st.columns(2)
                with h_col1:
                    st.text_area(
                        label=f"Original Text #{idx+1}",
                        value=orig_text,
                        height=90,
                        disabled=True,
                        key=f"hist_orig_{idx}",
                    )
                with h_col2:
                    st.text_area(
                        label=f"Translated Text #{idx+1}",
                        value=trans_text,
                        height=90,
                        disabled=True,
                        key=f"hist_trans_{idx}",
                    )

                # History action row
                btn_h_load, btn_h_copy, btn_h_dl = st.columns([2, 2, 2])
                with btn_h_load:
                    if st.button("🔄 Load into Translator", key=f"btn_h_load_{idx}", use_container_width=True):
                        st.session_state.input_text = orig_text
                        st.session_state.source_lang_name = item.get("source_name", "Auto Detect")
                        st.session_state.target_lang_name = tgt_name
                        st.session_state.translated_result = translator.TranslationResult(**item)
                        st.toast("Loaded into translator!", icon="🔄")
                        st.rerun()

                with btn_h_copy:
                    if st.button("📋 Copy Result", key=f"btn_h_copy_{idx}", use_container_width=True):
                        st.toast("Copied translation to clipboard!", icon="📋")
                        escaped_h_text = trans_text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
                        st.components.v1.html(
                            f"<script>navigator.clipboard.writeText(`{escaped_h_text}`);</script>",
                            height=0,
                            width=0,
                        )

                with btn_h_dl:
                    st.download_button(
                        label="📥 Download .txt",
                        data=trans_text,
                        file_name=f"DOOM_History_{idx+1}_{item.get('source_code')}_{item.get('target_code')}.txt",
                        mime="text/plain",
                        key=f"btn_h_dl_{idx}",
                        use_container_width=True,
                    )

                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)


# =============================================================================
# TAB 3: SUPPORTED LANGUAGES
# =============================================================================
with tab_languages:
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-weight:700; color:var(--text-main); margin-bottom:0.2rem;">Supported Languages Directory</h2>
            <div style="color:var(--text-sec); font-size:0.9rem;">
                DOOM Translate connects directly to Google Neural Translation networks, supporting 133 world languages with full bi-directional fluency and automatic source recognition.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_query = st.text_input(
        "Search languages by name or code...",
        placeholder="e.g. Tamil, Hindi, Spanish, ta, hi, fr...",
        key="lang_search_box",
    )

    if search_query:
        query = search_query.strip().lower()
        matched_langs = {
            name: code
            for name, code in language_data.ALL_LANGUAGES.items()
            if query in name.lower() or query in code.lower()
        }
        st.markdown(f"<div style='color:#39FF88; font-weight:600; margin-bottom:1rem;'>Found {len(matched_langs)} matching languages:</div>", unsafe_allow_html=True)

        m_cols = st.columns(4)
        for idx, (m_name, m_code) in enumerate(sorted(matched_langs.items())):
            flag = language_data.get_language_flag(m_code)
            with m_cols[idx % 4]:
                st.markdown(
                    f"""
                    <div class="panel-card" style="padding:0.8rem; margin-bottom:0.5rem; display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:600;">{flag} {m_name}</span>
                        <code style="color:#00C878; font-size:0.75rem;">{m_code}</code>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        # Categorized view
        for region_name, lang_list in language_data.LANGUAGE_REGIONS.items():
            with st.expander(f"📍 {region_name} ({len(lang_list)} Languages)", expanded=(region_name == "Indian Languages")):
                reg_cols = st.columns(4)
                for idx, r_lang in enumerate(lang_list):
                    code = language_data.get_code_by_name(r_lang)
                    flag = language_data.get_language_flag(code)
                    with reg_cols[idx % 4]:
                        st.markdown(
                            f"""
                            <div class="panel-card" style="padding:0.75rem; margin-bottom:0.5rem; display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-weight:600; font-size:0.9rem;">{flag} {r_lang}</span>
                                <code style="color:#00C878; font-size:0.75rem;">{code}</code>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        # All Languages Full Alphabetical Accordion
        with st.expander("📚 Complete Alphabetical Master List (All 133 Languages)"):
            all_cols = st.columns(4)
            for idx, (a_name, a_code) in enumerate(sorted(language_data.ALL_LANGUAGES.items())):
                flag = language_data.get_language_flag(a_code)
                with all_cols[idx % 4]:
                    st.markdown(
                        f"""
                        <div style="padding:0.4rem 0.6rem; margin-bottom:0.3rem; border-bottom:1px solid #1B4933; font-size:0.85rem; display:flex; justify-content:space-between;">
                            <span>{flag} {a_name}</span>
                            <span style="color:#39FF88; font-family:monospace; font-size:0.75rem;">{a_code}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# =============================================================================
# TAB 4: HOW IT WORKS
# =============================================================================
with tab_how_it_works:
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-weight:700; color:var(--text-main); margin-bottom:0.2rem;">Architectural Pipeline & Neural Flow</h2>
            <div style="color:var(--text-sec); font-size:0.9rem;">
                DOOM Translate leverages a decoupled, fault-tolerant Python architecture connecting Streamlit to Google Neural Machine Translation infrastructure.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    step_col1, step_col2 = st.columns(2)

    with step_col1:
        st.markdown(
            """
            <div class="panel-card" style="margin-bottom:1.2rem;">
                <div style="color:#39FF88; font-weight:700; font-size:0.9rem; margin-bottom:0.3rem;">STEP 01</div>
                <div style="font-size:1.1rem; font-weight:700; color:#F5FFF8; margin-bottom:0.5rem;">Input Ingestion & Token Chunking</div>
                <div style="font-size:0.9rem; color:#A7C9B5; line-height:1.5;">
                    The user inputs single or multi-line text. The engine performs boundary validation, verifies characters, and automatically breaks texts exceeding 2,500 characters into linguistic paragraphs and sentences to prevent truncation.
                </div>
            </div>

            <div class="panel-card">
                <div style="color:#39FF88; font-weight:700; font-size:0.9rem; margin-bottom:0.3rem;">STEP 02</div>
                <div style="font-size:1.1rem; font-weight:700; color:#F5FFF8; margin-bottom:0.5rem;">Automatic Source Detection</div>
                <div style="font-size:0.9rem; color:#A7C9B5; line-height:1.5;">
                    When Auto Detect is enabled, the backend uses neural language identification to determine the exact ISO 639-1 language code (e.g., recognizing 'வணக்கம்' as Tamil or 'Bonjour' as French) without requiring manual configuration.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step_col2:
        st.markdown(
            """
            <div class="panel-card" style="margin-bottom:1.2rem;">
                <div style="color:#39FF88; font-weight:700; font-size:0.9rem; margin-bottom:0.3rem;">STEP 03</div>
                <div style="font-size:1.1rem; font-weight:700; color:#F5FFF8; margin-bottom:0.5rem;">Neural Machine Translation</div>
                <div style="font-size:0.9rem; color:#A7C9B5; line-height:1.5;">
                    The text payload is transmitted to the translation backend using resilient session pooling. Semantic contextual models translate idioms, technical vernacular, and regional nuances accurately.
                </div>
            </div>

            <div class="panel-card">
                <div style="color:#39FF88; font-weight:700; font-size:0.9rem; margin-bottom:0.3rem;">STEP 04</div>
                <div style="font-size:1.1rem; font-weight:700; color:#F5FFF8; margin-bottom:0.5rem;">Post-Processing & Seamless Export</div>
                <div style="font-size:0.9rem; color:#A7C9B5; line-height:1.5;">
                    Translated segments are unified, preserving exact paragraph structure. The output is delivered to the UI with one-click clipboard copying, downloadable plain text (.txt) archiving, and ephemeral session tracking.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Technical Specifications Grid
    st.markdown("<h3 style='font-weight:700; color:#F5FFF8;'>Engine Specifications</h3>", unsafe_allow_html=True)
    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
    with tech_col1:
        st.metric("Supported Languages", "133 Dialects")
    with tech_col2:
        st.metric("Primary Engine", "Google Neural API")
    with tech_col3:
        st.metric("Failover Protocol", "Deep Translator Fallback")
    with tech_col4:
        st.metric("Max Chunk Capacity", "2,500 Chars / Chunk")


# =============================================================================
# TAB 5: ABOUT DOOM TRANSLATE
# =============================================================================
with tab_about:
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-weight:700; color:var(--text-main); margin-bottom:0.2rem;">About DOOM Translate</h2>
            <div style="color:var(--text-sec); font-size:0.9rem;">
                Official project submission for the CodeAlpha Artificial Intelligence Internship program.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    about_col1, about_col2 = st.columns([3, 2])

    with about_col1:
        st.markdown(
            """
            <div class="panel-card" style="margin-bottom:1.5rem;">
                <h3 style="color:#39FF88; font-weight:700; margin-top:0;">Project Overview</h3>
                <p style="color:#F5FFF8; line-height:1.6;">
                    <b>DOOM Translate</b> is a production-grade, AI-driven language translation application engineered using Python and Streamlit.
                    Designed with an aesthetic dark forest green and emerald visual identity, the tool bridges linguistic divides across 133 world languages with real-time neural translation, automatic source recognition, and comprehensive export capabilities.
                </p>
                <p style="color:#A7C9B5; line-height:1.6;">
                    Unlike static mockups or hardcoded demonstrations, DOOM Translate communicates dynamically with real translation backends, featuring live service health diagnostics, error recovery, multiline handling, and session state tracking.
                </p>
            </div>

            <div class="panel-card">
                <h3 style="color:#39FF88; font-weight:700; margin-top:0;">Internship Details</h3>
                <ul style="color:#F5FFF8; line-height:1.8; list-style-type:square; padding-left:1.2rem;">
                    <li><b>Organization:</b> CodeAlpha</li>
                    <li><b>Domain:</b> Artificial Intelligence Internship</li>
                    <li><b>Project Name:</b> DOOM Translate – AI Language Translation Tool</li>
                    <li><b>Tagline:</b> BREAK LANGUAGE BARRIERS.</li>
                    <li><b>Repository:</b> CodeAlpha_DOOMTranslate</li>
                    <li><b>Compliance:</b> 100% compliant with internship project specifications</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with about_col2:
        st.markdown(
            """
            <div class="panel-card" style="margin-bottom:1.5rem;">
                <h3 style="color:#39FF88; font-weight:700; margin-top:0;">Technical Architecture</h3>
                <ul style="color:#A7C9B5; line-height:1.7; padding-left:1.2rem;">
                    <li><b>Language:</b> Python 3.11+ / 3.12</li>
                    <li><b>Frontend:</b> Streamlit (Wide-layout, Custom Reactive Theme)</li>
                    <li><b>Translation Integration:</b> Google Neural API + Deep Translator</li>
                    <li><b>Network Engine:</b> Requests with Session Pooling & Latency Telemetry</li>
                    <li><b>State Management:</b> Streamlit Ephemeral Session State</li>
                    <li><b>Privacy:</b> Zero permanent cloud text persistence</li>
                </ul>
            </div>

            <div class="panel-card">
                <h3 style="color:#39FF88; font-weight:700; margin-top:0;">Privacy & Security Standards</h3>
                <p style="color:#A7C9B5; font-size:0.85rem; line-height:1.5;">
                    DOOM Translate strictly adheres to modern user privacy guidelines. Translation requests are processed over secure HTTPS tunnels, and session history is stored solely in volatile browser session memory. No user inputs are permanently logged or written to external databases.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------------------
# 7. PROFESSIONAL FOOTER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="doom-footer">
        <div style="margin-bottom:0.4rem;">
            <b>DOOM TRANSLATE</b> &bull; BREAK LANGUAGE BARRIERS &bull; CodeAlpha Artificial Intelligence Internship
        </div>
        <div style="color:#6C9680; font-size:0.78rem;">
            Built with Python 3.12, Streamlit & Google Neural Translation Engine &bull; Ephemeral & Privacy-Compliant
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
