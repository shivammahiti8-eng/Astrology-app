from datetime import datetime, time
import json
import urllib.error
import urllib.request
import streamlit as st

# 1. Page Configuration & Custom Mystical Dark UI
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
        background: linear-gradient(135deg, #090614 0%, #120b29 50%, #1e0a2d 100%);
        color: #e2e8f0;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(12, 8, 24, 0.95) !important;
        border-right: 1px solid rgba(229, 193, 88, 0.25);
    }
    .stChatMessage {
        border-radius: 12px !important;
        padding: 14px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(126, 34, 206, 0.15) !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(229, 193, 88, 0.25) !important;
    }
    .stChatInputContainer {
        border-radius: 16px !important;
        border: 1px solid rgba(229, 193, 88, 0.4) !important;
    }
    .title-text {
        background: linear-gradient(90deg, #fef08a 0%, #d97706 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 2. Sidebar Setup & Key Sanitization
st.sidebar.markdown("## 🔮 Astrological Profile")

birth_date = st.sidebar.date_input("Date of Birth", value=datetime(2008, 12, 26))
birth_time = st.sidebar.time_input("Time of Birth", value=time(6, 30))
birth_place = st.sidebar.text_input(
    "Place of Birth", value="Bhandara Road, Maharashtra"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🪐 Chart Parameters")
st.sidebar.markdown("**Lagna (Ascendant):** Sagittarius / Dhanu 🏹")
st.sidebar.markdown("**Moon Sign (Rashi):** Scorpio / Vrischika 抓")
st.sidebar.markdown("**Lagna Lord:** Jupiter (Guru)")
st.sidebar.markdown("---")

# Retrieve secret if set, or let user input it
default_key = ""
if "GEMINI_API_KEY" in st.secrets:
    default_key = str(st.secrets["GEMINI_API_KEY"])

st.sidebar.markdown("### 🔑 AI Connection")
raw_api_key = st.sidebar.text_input(
    "Enter Gemini API Key:",
    value=default_key,
    type="password",
    help="Get your free key at aistudio.google.com",
)

# Clean and sanitize API key string (strips whitespace, quotes, or accidental prefixes)
clean_api_key = (
    raw_api_key.strip()
    .replace('"', "")
    .replace("'", "")
    .replace("GEMINI_API_KEY =", "")
    .strip()
)

if st.sidebar.button("🗑️ Clear Chat / Start New Session"):
    st.session_state.messages = []
    st.rerun()

# 3. Main Interface Header
st.markdown(
    "<h1 class='title-text'>🌌 Vedic Cosmic AI Astrologer</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #a7f3d0;'>Conversational Jyotish Intelligence • Past Verification Engine • Deep Future Dynamics</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Quick Prompt Helper Button for Past Verification
col1, col2 = st.columns(2)
with col1:
    if st.button("📜 Verify My Past (Peep Into History)"):
        st.session_state.pending_prompt = "Analyze my past life phases over the last 3-5 years (e.g., 2021 to 2025) using my Dasha timeline and major transits. Describe what shifts occurred in my mindset, health, education, or personal life so I can verify your accuracy."
with col2:
    if st.button("🔮 Forecast My Future Horizons"):
        st.session_state.pending_prompt = "Analyze my upcoming planetary transits and Dasha cycles for the next 12 to 36 months. Break down career, physical growth, wealth compounding, and major life timing."

# 4. Master System Instruction (Vedic Expert + Past Verification Mandate)
SYSTEM_INSTRUCTION = f"""
You are an expert, deeply analytical Vedic Astrologer with 70 years of experience in Parashari Jyotish, Jaimini Sutras, Dashas, and Gochar (planetary transits). 
You are speaking directly to a seeker with the following birth chart details:
- Date of Birth: {birth_date.strftime("%d December %Y")}
- Time of Birth: {birth_time.strftime("%I:%M %p")}
- Place of Birth: {birth_place}
- Lagna (Ascendant): Sagittarius (Dhanu) - Ruled by Jupiter
- Moon Sign (Rashi): Scorpio (Vrischika) - Ruled by Mars

CORE MANDATES:
1. PAST RETROSPECTIVE VERIFICATION (PEEPING INTO THE PAST):
   - Whenever asked about past events or general predictions, include a dedicated "📜 Past Timeline Verification" section.
   - Calculate past Mahadashas, Antardashas, and major planetary transits (e.g., Saturn's Sade Sati / Kantaka Shani, Rahu-Ketu axis shifts, Jupiter transits) for key past years (2020-2025).
   - Detail specific past psychological themes, emotional trials, academic/career pivots, or health/stamina shifts. This past accuracy builds absolute trust so the seeker can verify your logic against their real experience before looking ahead.

2. HIGH-DEPTH UNRESTRICTED ANALYSIS:
   - Provide comprehensive, highly descriptive, and deeply analytical readings. Avoid short, generic horoscopes.
   - Explain specific house lordships, aspects (Drishti), transit dynamics, and practical psychological/actionable remedies.

3. CONVERSATIONAL MEMORY & DYNAMIC FOLLOW-UPS:
   - Maintain full awareness of previous messages in this conversation.
   - ALWAYS END EVERY RESPONSE with a section formatted exactly like this:

---
### 🔮 Suggested Follow-Up Questions:
* [Option 1: A deep logical question verifying a specific past timeframe]
* [Option 2: A question exploring upcoming transit timing or horizons]
* [Option 3: A practical question regarding physical growth, remedies, or strategy]
"""


# Direct REST API Engine targeting updated gemini-2.5-flash endpoint
def call_gemini_api(key, system_instruction, chat_history, current_prompt):
    # Updated to gemini-2.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"

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
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        error_info = e.read().decode("utf-8")
        raise Exception(f"API Error ({e.code}): {error_info}")
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


# 5. Chat History & Logic Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture input from chat box or prompt helper buttons
user_prompt = st.chat_input(
    "Ask anything about your past years, future transits, career, or life..."
)

if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    user_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_prompt:
    if not clean_api_key:
        st.warning(
            "⚠️ Please enter or paste your Gemini API Key in the left sidebar to start!"
        )
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner(
            "Analyzing past Dasha timelines, transits, and planetary positions..."
        ):
            try:
                response_text = call_gemini_api(
                    clean_api_key,
                    SYSTEM_INSTRUCTION,
                    st.session_state.messages[:-1],
                    user_prompt,
                )
                st.markdown(response_text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
    
