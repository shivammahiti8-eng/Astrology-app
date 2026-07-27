from datetime import datetime, time
import json
import urllib.error
import urllib.request
import streamlit as st

# 1. Page Configuration & Custom Mystical Glassmorphism UI
st.set_page_config(
    page_title="Vedic AI Cosmic Guru",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Dark Cosmic Chat Interface
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

# 2. Sidebar: Birth Chart Profile & API Key
st.sidebar.markdown("## 🔮 Astrological Profile")

birth_date = st.sidebar.date_input("Date of Birth", value=datetime(2008, 12, 26))
birth_time = st.sidebar.time_input("Time of Birth", value=time(6, 30))
birth_place = st.sidebar.text_input(
    "Place of Birth", value="Bhandara Road, Maharashtra"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🪐 Chart Parameters")
st.sidebar.markdown("**Lagna (Ascendant):** Sagittarius / Dhanu 🏹")
st.sidebar.markdown("**Moon Sign (Rashi):** Scorpio / Vrischika 🦂")
st.sidebar.markdown("**Lagna Lord:** Jupiter (Guru)")
st.sidebar.markdown("---")

# API Key input for Gemini AI Engine
st.sidebar.markdown("### 🔑 AI Connection")
api_key = st.sidebar.text_input(
    "Enter Gemini API Key:",
    type="password",
    help="Get your free API key at aistudio.google.com to power full conversational AI depth.",
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
    "<p style='text-align: center; color: #a7f3d0;'>Conversational Jyotish Intelligence • Full Memory • Dynamic Follow-ups</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# 4. System Instruction for Gemini
SYSTEM_INSTRUCTION = f"""
You are an expert, deeply analytical Vedic Astrologer with 70 years of experience in Parashari Jyotish, Jaimini Sutras, Dashas, and Gochar (planetary transits). 
You are speaking directly to a seeker with the following fixed birth chart details:
- Date of Birth: {birth_date.strftime("%d December %Y")}
- Time of Birth: {birth_time.strftime("%I:%M %p")}
- Place of Birth: {birth_place}
- Lagna (Ascendant): Sagittarius (Dhanu) - Ruled by Jupiter
- Moon Sign (Rashi): Scorpio (Vrischika) - Ruled by Mars

YOUR MANDATE:
1. Provide EXTREMELY HIGH DEPTH, DESCRIPTIVE, and UNRESTRICTED astrological analysis. Avoid short, generic, surface-level horoscopes.
2. Calculate and discuss specific planetary dynamics: House Lordship, Aspects (Drishti), Mahadasha/Antardasha influences, and Transit cycles (Saturn/Shani, Jupiter/Guru, Rahu/Ketu).
3. Connect astrological principles directly to practical psychological insights, career vectors, physical stamina/health, wealth compounding, and long-term timing over the next 30 years.
4. Maintain full conversational context—refer back to previous questions or topics discussed in the chat history.
5. ALWAYS END EVERY SINGLE RESPONSE with a dedicated section formatted exactly like this:

---
### 🔮 Suggested Follow-Up Questions:
* [Option 1: A deep logical follow-up question related to what was just discussed]
* [Option 2: A question exploring a specific timing or transit horizon]
* [Option 3: A question regarding remedies, mindset, or practical steps]
"""


# Direct REST API helper (uses Python standard library, requiring no pip packages)
def call_gemini_api(key, system_instruction, chat_history, current_prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"

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
        raise Exception(f"API Key or Request Error ({e.code}): {error_info}")
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


# 5. Initialize Chat History Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages from memory
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input & AI Generation Logic
if user_prompt := st.chat_input(
    "Ask any detailed question about your Kundali, transits, career, life, or future..."
):

    if not api_key.strip():
        st.warning(
            "⚠️ Please enter your free Gemini API Key in the left sidebar to start chatting!"
        )
        st.stop()

    # Add User Message to Chat UI & Session Memory
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Call Gemini via direct API request
    with st.chat_message("assistant"):
        with st.spinner(
            "Analyzing Kundali, house lords, and transit matrices..."
        ):
            try:
                response_text = call_gemini_api(
                    api_key.strip(),
                    SYSTEM_INSTRUCTION,
                    st.session_state.messages[:-1],
                    user_prompt,
                )
                st.markdown(response_text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
            except Exception as e:
                st.error(f"Error generating reading: {str(e)}")
