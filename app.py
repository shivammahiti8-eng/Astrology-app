from datetime import datetime, time, timedelta
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Vedic Transit & Prediction Engine",
    page_icon="🔮",
    layout="centered",
)

st.title("🔮 AI Vedic Astrology & 30-Year Transit Engine")
st.write(
    "Ask any question or search any topic to get real-time planetary guidance and transit analysis."
)

# 2. Sidebar: Fixed Default Birth Information
st.sidebar.header("👤 Your Birth Profile")
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
st.sidebar.markdown("**Ascendant (Lagna):** Sagittarius / Dhanu")
st.sidebar.markdown("**Moon Sign (Rashi):** Scorpio / Vrischika")

# 3. Target Date Selection
st.subheader("📅 Step 1: Choose Time Horizon")
today = datetime.today().date()
max_future_date = today + timedelta(days=365 * 30)

target_date = st.date_input(
    "Select target date for your reading (up to 30 years ahead):",
    value=today,
    min_value=today,
    max_value=max_future_date,
)

# 4. Interactive Question Search Bar
st.subheader("❓ Step 2: Search or Ask Any Question")
user_question = st.text_input(
    "Type your question below:",
    placeholder="e.g., 'How will my career look in 2028?', 'Will I clear my exams?', 'What about health & fitness?'",
)


# 5. Astrological Interpretation Engine
def analyze_question_and_transit(question, target_dt, bdate):
    age = target_dt.year - bdate.year
    q_lower = question.lower()

    # Dynamic Categorization based on Query Keywords
    if any(
        w in q_lower
        for w in [
            "job",
            "career",
            "work",
            "business",
            "exam",
            "study",
            "success",
            "future",
            "pass",
            "score",
        ]
    ):
        topic = "Career, Education & Karma Vector"
        house = "10th House (Karma Bhava) & 5th House (Vidya Bhava)"
        primary_planet = "Jupiter (Guru) & Saturn (Shani)"
        guidance = (
            f"Around age {age}, your planetary transits heavily reward structured discipline and technical skill building. "
            "Saturn demands consistent daily execution without shortcuts, while Jupiter creates opportunities for recognition. "
            "Focus on long-term skill compounding rather than immediate validation."
        )
    elif any(
        w in q_lower
        for w in [
            "money",
            "wealth",
            "finance",
            "rich",
            "income",
            "gain",
            "car",
            "house",
            "buy",
        ]
    ):
        topic = "Wealth, Assets & Expansion"
        house = "2nd House (Dhana Bhava) & 11th House (Labha Bhava)"
        primary_planet = "Mercury (Budh) & Venus (Shukra)"
        guidance = (
            f"At age {age}, financial growth aligns with logical planning and strategic investments. "
            "Avoid high-risk speculation during key Rahu cycles; focus instead on compounding assets, clear budgeting, and building solid income streams."
        )
    elif any(
        w in q_lower
        for w in [
            "love",
            "marriage",
            "partner",
            "relationship",
            "girl",
            "friend",
            "trust",
        ]
    ):
        topic = "Relationships, Trust & Partnerships"
        house = "7th House (Yuvati Bhava) & 5th House (Kama Bhava)"
        primary_planet = "Venus (Shukra) & Jupiter (Guru)"
        guidance = (
            "Transits emphasize emotional clarity, mutual respect, and humor. "
            "Relationships thrive when grounded in strong friendship first. Keep communication logic-driven, honest, and supportive."
        )
    elif any(
        w in q_lower
        for w in [
            "health",
            "fitness",
            "body",
            "gym",
            "mind",
            "stress",
            "energy",
            "workout",
        ]
    ):
        topic = "Health, Physical Vitality & Mindset"
        house = "1st House (Tanu Bhava) & 6th House (Arogya Bhava)"
        primary_planet = "Sun (Surya) & Mars (Mangal)"
        guidance = (
            f"Physical strength and mental endurance are highlighted for {target_dt.year}. "
            "Mars transit energy supports intensive physical conditioning, body building, and disciplined routines. Channel high energy into heavy physical training."
        )
    else:
        topic = "General Destiny & Life Cycle Direction"
        house = "1st House (Self Evolution) & 9th House (Bhagya Bhava)"
        primary_planet = "Jupiter (Guru Alignment) & Rahu/Ketu Axis"
        guidance = (
            f"Looking at your chart for {target_dt.strftime('%B %Y')} (Age ~{age}), overall planetary transits urge self-mastery, "
            "building personal strength, and executing long-term projects. Focus on aligning daily action with your ultimate growth vector."
        )

    return topic, house, primary_planet, guidance


# 6. Action Button
if st.button("🔮 Analyze Planetary Transit Energy"):
    if not user_question.strip():
        st.warning(
            "Please type a question in the search bar above to generate a tailored reading!"
        )
    else:
        st.markdown("---")
        st.success(
            f"**Reading Generated for Target Date:** {target_date.strftime('%d %B %Y')}"
        )

        topic, house, primary_planet, guidance = analyze_question_and_transit(
            user_question, target_date, birth_date
        )

        st.markdown(f"### 🎯 Query: *\"{user_question}\"*")

        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Birth Place:** {birth_place}")
            st.info(
                f"**Birth Details:** {birth_date.strftime('%d-%m-%Y')} | {birth_time.strftime('%I:%M %p')}"
            )
            st.info(f"**Core Topic:** {topic}")
        with col2:
            st.info(
                f"**Target Year:** {target_date.year} (Age ~{target_date.year - birth_date.year})"
            )
            st.info(f"**Active House Focus:** {house}")
            st.info(f"**Key Planets:** {primary_planet}")

        st.subheader("📜 Detailed Transit Analysis & Prediction")
        st.write(guidance)

        st.subheader("💡 Strategic Action Plan")
        st.markdown("""
        * **Primary Focus:** Leverage disciplined daily action (Saturn) guided by clear vision (Jupiter).
        * **Mindset:** Use challenges as direct fuel for skill development and personal strength.
        * **Core Rule:** Action creates outcomes—planetary positions show where energy flows, but your choices dictate the result.
        """)
            
