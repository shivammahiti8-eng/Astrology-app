from datetime import datetime, time
import streamlit as st

# Safe import to prevent red error screens
try:
    import google.generativeai as genai

    HAS_GENAI = True
except ModuleNotFoundError:
    HAS_GENAI = False

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

# Package Missing Alert
if not HAS_GENAI:
    st.warning(
        "⚠️ `google-generativeai` package is currently installing... Please make sure `requirements.txt` is committed on GitHub and tap 'Reboot App' in Streamlit menu if needed!"
    )

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

    if not api_key:
        st.warning(
            "⚠️ Please enter a free Gemini API Key in the left sidebar to start chatting! (Get one in 10 seconds at aistudio.google.com)"
        )
        st.stop()

    if not HAS_GENAI:
        st.error(
            "⚠️ Installing `google-generativeai` package on Streamlit server... Please wait a few seconds and try again!"
        )
        st.stop()

    # Add User Message to Chat UI & Session Memory
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Configure Gemini AI Engine
    try:
        genai.configure(api_key=api_key)

        # Reconstruct chat history for Gemini to ensure true context memory
        gemini_history = []
        for msg in st.session_state.messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        # Load Gemini Model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_INSTRUCTION,
        )

        chat_session = model.start_chat(history=gemini_history)

        # Generate Deep AI Response
        with st.chat_message("assistant"):
            with st.spinner(
                "Analyzing Kundali, house lords, and transit matrices..."
            ):
                response = chat_session.send_message(user_prompt)
                response_text = response.text
                st.markdown(response_text)

        # Append Assistant Response to Session Memory
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )

    except Exception as e:
        st.error(
            f"An error occurred while connecting to Gemini AI: {str(e)}. Please check your API Key."
)
