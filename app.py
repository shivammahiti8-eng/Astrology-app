from datetime import datetime, time, timedelta
import streamlit as st

# Optional Gemini AI import
try:
    import google.generativeai as genai

    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# 1. Page Config & Mystical Theme Styling (CSS)
st.set_page_config(
    page_title="Vedic Cosmic AI Astrologer",
    page_icon="✨",
    layout="centered",
)

# Custom Dark Mystical Background & UI Styles
st.markdown(
    """
<style>
    /* Dark Cosmic Background */
    .stApp {
        background: linear-gradient(135deg, #0b081a 0%, #160f2e 50%, #230f38 100%);
        color: #e2e8f0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 10, 30, 0.95) !important;
        border-right: 1px solid rgba(229, 193, 88, 0.25);
    }
    
    /* Glowing Action Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #7e22ce 0%, #d97706 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(217, 119, 6, 0.35) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5) !important;
    }
    
    /* Cosmic Glassmorphism Containers */
    .mystic-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(229, 193, 88, 0.3);
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f3e8ff !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 2. Main Title Header
st.markdown(
    "<h1 style='text-align: center;'>✨ Cosmic AI Vedic Astrologer ✨</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #cbd5e1;'>Deep 30-Year Planetary Transit Analysis & Detailed Predictions</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# 3. Sidebar: Birth Details & Optional AI Key
st.sidebar.header("🔮 Birth Chart Profile")
birth_date = st.sidebar.date_input(
    "Date of Birth",
    value=datetime(2008, 12, 26),
    min_value=datetime(1950, 1, 1),
)
birth_time = st.sidebar.time_input("Time of Birth", value=time(6, 30))
birth_place = st.sidebar.text_input(
    "Place of Birth", value="Bhandara Road, Maharashtra"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Lagna (Ascendant):** Sagittarius / Dhanu")
st.sidebar.markdown("**Moon Sign (Rashi):** Scorpio / Vrischika")
st.sidebar.markdown("---")

# Optional Gemini API Key Input for Unlimited AI Depth
st.sidebar.header("🔑 AI Integration (Optional)")
gemini_api_key = st.sidebar.text_input(
    "Paste Free Gemini API Key:",
    type="password",
    help="Get a 100% free key from aistudio.google.com to unlock unlimited AI deep reading generation!",
)

# 4. Target Horizon & Search/Question Input
st.subheader("📅 Step 1: Select Target Date Horizon")
today = datetime.today().date()
max_future_date = today + timedelta(days=365 * 30)

target_date = st.date_input(
    "Choose any date up to 30 years into the future:",
    value=today,
    min_value=today,
    max_value=max_future_date,
)

st.subheader("❓ Step 2: Search or Ask Any Question")
user_question = st.text_input(
    "Ask your question below:",
    placeholder="e.g., 'Detailed career roadmap for 2029?', 'How will my body & physical health evolve?', 'What about wealth?'",
)


# 5. AI Generation Function
def generate_ai_prediction(question, t_date, b_date, b_time, b_place, api_key):
    age = t_date.year - b_date.year

    prompt = f"""
    You are an AI Vedic Astrologer with 70 years of wisdom, grounded in Parashari Jyotish, Dasha systems, and Gochar (planetary transits).

    USER BIRTH PROFILE:
    - Date of Birth: {b_date.strftime("%d %B %Y")}
    - Time of Birth: {b_time.strftime("%I:%M %p")}
    - Place of Birth: {b_place}
    - Lagna (Ascendant): Sagittarius (Dhanu)
    - Moon Sign (Rashi): Scorpio (Vrischika)

    PREDICTION HORIZON:
    - Target Date: {t_date.strftime("%d %B %Y")} (User will be approximately {age} years old)

    USER QUESTION: "{question}"

    INSTRUCTIONS:
    Provide an exhaustive, highly detailed, descriptive, and integrated Vedic astrological interpretation addressing their question specifically for this time horizon.
    
    Structure your detailed reading into 3 distinct sections:
    1. 🪐 Planetary Energy & Transit Matrix (Explain active house influences, Jupiter/Saturn/Rahu dynamics for age {age}).
    2. 📜 In-Depth Narrative Analysis (Provide an extensive, highly detailed descriptive breakdown answering their specific query).
    3. 💡 Strategic Cosmic Guidance (Actionable steps, mindset adjustments, and remedies to maximize success).
    
    Use a wise, encouraging, mystical, yet grounded and practical tone.
    """

    if api_key and HAS_GENAI:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(
                f"AI Key Error: {str(e)}. Falling back to local internal engine."
            )

    # Fallback Internal Engine if no API key is provided
    return f"""
    ### 🪐 1. Planetary Energy & Transit Matrix
    * **Active Transit Focus:** For **{t_date.strftime("%d %B %Y")}** (Age ~{age}), your chart experiences strong transits affecting key house axes from **{b_place}**.
    * **Saturn (Shani) Alignment:** Demands strict daily discipline, physical/mental endurance, and structured effort without shortcuts.
    * **Jupiter (Guru) Alignment:** Illuminates expansion, skill mastery, and alignment with wisdom and career breakthroughs.

    ### 📜 2. In-Depth Narrative Analysis
    Regarding your focus on **"{question}"**:
    During this target period in **{t_date.year}**, the planetary energies demand that you synthesize long-term vision with deliberate daily action. 
    Because your Lagna is Sagittarius and Moon Sign is Scorpio, you possess deep emotional resilience combined with an innate drive for high achievement. 
    
    This phase requires you to avoid short-term distractions. If you are asking about career, studies, or personal development, Saturn's transit ensures that every hour of effort put in will compound into lasting authority. If asking about physical conditioning, Mars energy favors intense physical training and high vital stamina.

    ### 💡 3. Strategic Cosmic Guidance
    * **Core Mantra:** "Consistency creates destiny." The planets indicate potential, but your deliberate habits activate the highest outcomes.
    * **Action Vector:** Maintain structured daily routines, prioritize continuous learning, and build physical and mental strength.
    
    *(Tip: For unlimited multi-page AI customized readings, paste a free Gemini API key in the sidebar!)*
    """


# 6. Action Button & Output Render
if st.button("🔮 Unveil Cosmic Reading"):
    if not user_question.strip():
        st.warning("Please type a question in the search bar above!")
    else:
        st.markdown("---")
        with st.spinner("Calculating planetary transits and generating AI reading..."):
            reading = generate_ai_prediction(
                user_question,
                target_date,
                birth_date,
                birth_time,
                birth_place,
                gemini_api_key,
            )

        st.markdown(
            f"""
        <div class="mystic-card">
            <h2 style="color: #ffd700 !important; margin-top:0;">🔮 Cosmic Analysis for {target_date.strftime("%B %d, %Y")}</h2>
            <p><strong>Query:</strong> <em>"{user_question}"</em></p>
            <p><strong>Profile:</strong> {birth_place} | {birth_date.strftime("%d-%m-%Y")} at {birth_time.strftime("%I:%M %p")}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(reading)
    
        
