from datetime import datetime, time
import json
import time as t_module
import urllib.error
import urllib.request
import streamlit as st

# 1. Page Configuration & Custom High-Contrast Dark UI
st.set_page_config(
    page_title="Vedic AI Cosmic Guru",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0618 0%, #11092b 50%, #1a0826 100%);
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #0c081d !important;
        border-right: 1px solid rgba(234, 179, 8, 0.3);
    }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label {
        color: #f1f5f9 !important;
    }
    .stChatMessage {
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
        color: #f8fafc !important;
    }
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(88, 28, 135, 0.45) !important;
        border: 1px solid #a855f7 !important;
        color: #ffffff !important;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid #eab308 !important;
        color: #f8fafc !important;
    }
    div[data-testid="stChatMessage"] p, 
    div[data-testid="stChatMessage"] li, 
    div[data-testid="stChatMessage"] span, 
    div[data-testid="stChatMessage"] h1, 
    div[data-testid="stChatMessage"] h2, 
    div[data-testid="stChatMessage"] h3 {
        color: #f8fafc !important;
    }
    .stButton>button {
        color: #fef08a !important;
        background-color: #1e1b4b !important;
        border: 1px solid #eab308 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #312e81 !important;
        border-color: #fde047 !important;
        color: #ffffff !important;
    }
    .title-text {
        background: linear-gradient(90deg, #fef08a 0%, #f59e0b 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
    }
    .sub-text {
        color: #38bdf8 !important;
        text-align: center;
        font-weight: 500;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 2. Sidebar Setup & Profile Parameters
st.sidebar.markdown("## 🔮 Astrological Profile")

birth_date = st.sidebar.date_input("Date of Birth", value=datetime(2008, 12, 26))
birth_time = st.sidebar.time_input("Time of Birth", value=time(6, 30))
birth_place = st.sidebar.text_input(
    "Place of Birth", value="Bhandara Road, Maharashtra"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🪐 Chart Parameters")
st.sidebar.markdown("**Lagna (Ascendant):** Sagittarius / Dhanu 🏹")
st.sidebar.markdown("**Moon Sign (Rashi):** Scorpio / Vrischika ♏")
st.sidebar.markdown("**Lagna Lord:** Jupiter (Guru)")
st.sidebar.markdown("---")

# Load Multiple API Keys from Secrets
api_keys_list = []
if "GEMINI_API_KEYS" in st.secrets:
    raw_keys = str(st.secrets["GEMINI_API_KEYS"])
    api_keys_list = [k.strip().replace('"', "").replace("'", "") for k in raw_keys.split(",") if k.strip()]
elif "GEMINI_API_KEY" in st.secrets:
    api_keys_list = [str(st.secrets["GEMINI_API_KEY"]).strip().replace('"', "").replace("'", "")]

if st.sidebar.button("🗑️ Clear Chat / Start New Session"):
    st.session_state.messages = []
    st.rerun()

# 3. Main Interface Header
st.markdown(
    "<h1 class='title-text'>🌌 Vedic Cosmic AI Astrologer</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='sub-text'>Autonomous Jyotish Intelligence • Dual-Model & Multi-Key Failover Engine (2008–2020)</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("📜 Verify My Past (2008 to 2020 Retrospective)"):
        st.session_state.pending_prompt = "Analyze my past life phases strictly from my birth year (2008) up to 2020 using my Dasha timeline and planetary transits. Detail the psychological shifts, childhood development, health, and family/academic dynamics across these exact years (2008-2020) so I can verify your accuracy."
with col2:
    if st.button("🔮 Forecast My Future Horizons"):
        st.session_state.pending_prompt = "Analyze my upcoming planetary transits and Dasha cycles for the next 12 to 36 months. Break down career, physical growth, wealth compounding, and major life timing."

# 4. Master System Instruction
SYSTEM_INSTRUCTION = f"""
You are an expert, deeply analytical Vedic Astrologer with 70 years of experience in Parashari Jyotish, Jaimini Sutras, Dashas, and Gochar (planetary transits). 
You are speaking directly to a seeker with the following birth chart details:
- Date of Birth: {birth_date.strftime("%d December %Y")}
- Time of Birth: {birth_time.strftime("%I:%M %p")}
- Place of Birth: {birth_place}
- Lagna (Ascendant): Sagittarius (Dhanu) - Ruled by Jupiter
- Moon Sign (Rashi): Scorpio (Vrischika) - Ruled by Mars

CORE MANDATES:
1. PAST RETROSPECTIVE VERIFICATION (EXCLUSIVELY 2008 TO 2020):
   - When asked about past events or general verification, focus EXCLUSIVELY on the timeline from birth year (2008) UP TO 2020 ONLY.
   - Calculate Mahadashas, Antardashas, and key planetary transits (e.g., Saturn transits, Rahu-Ketu shifts, Jupiter transits) during 2008–2020.
   - Describe specific psychological themes, childhood developments, academic shifts, health factors, or family environment changes during these exact years (2008-2020).
   - This precise past accuracy allows the seeker to cross-check your astrological logic with their real past experiences up to 2020 before accepting future forecasts.

2. HIGH-DEPTH UNRESTRICTED ANALYSIS:
   - Provide clear, well-structured, and deeply analytical readings. Avoid vague or generic horoscopes.
   - Explain house lordships, aspects (Drishti), transit dynamics, and practical actionable remedies.

3. CONVERSATIONAL MEMORY & DYNAMIC FOLLOW-UPS:
   - Maintain full awareness of previous messages in this conversation session.
   - ALWAYS END EVERY RESPONSE with a section formatted exactly like this:

---
### 🔮 Suggested Follow-Up Questions:
* [Option 1: A specific question cross-checking a year between 2008 and 2020]
* [Option 2: A question exploring upcoming transit timing or horizons]
* [Option 3: A practical question regarding remedies, focus, or growth strategy]
"""


# 5. Advanced Engine with Cross-Model Fallback & Key Rotation
def call_gemini_api_advanced(keys_list, system_instruction, chat_history, current_prompt):
    if not keys_list:
        raise Exception("No API keys found in Streamlit secrets configuration.")

    contents = []
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    contents.append({"role": "user", "parts": [{"text": current_prompt}]})

    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": contents,
    }
    data = json.dumps(payload).encode("utf-8")

    # Try multiple models to bypass individual model pool limits
    models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash"]

    for model in models_to_try:
        for key in keys_list:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            req = urllib.request.Request(
                url, data=data, headers={"Content-Type": "application/json"}
            )

            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    return result["candidates"][0]["content"]["parts"][0]["text"]
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8")
                if e.code == 429:
                    # Rate limit hit, try next key/model immediately
                    t_module.sleep(0.5)
                    continue
                else:
                    # Non-429 error, try next
                    continue
            except Exception:
                continue

    raise Exception("All keys and fallback model quotas are temporarily exhausted. Please wait 15 seconds.")


# 6. Chat History & Execution Loop
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input(
    "Ask anything about your past (2008-2020), future transits, career, or life..."
)

if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    user_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_prompt:
    if not api_keys_list:
        st.error(
            "⚙️ **Configuration Required:** Please add your `GEMINI_API_KEYS` (separated by commas) into your Streamlit Cloud App Settings under 'Secrets'."
        )
