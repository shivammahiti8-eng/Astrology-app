# 1. Page Configuration
st.set_page_config(
    page_title="30-Year Planetary Transit Engine",
    page_icon="🌌",
    layout="centered",
)

st.title("🌌 30-Year Planetary Transit & Life Focus Engine")
st.write(
    "Analyze major planetary transits (Saturn, Jupiter, Rahu/Ketu) for any day over the next 30 years."
)

# 2. Sidebar: User Birth Information
st.sidebar.header("👤 Enter Birth Details")
birth_date = st.sidebar.date_input(
    "Date of Birth", value=datetime(2000, 1, 1), min_value=datetime(1950, 1, 1)
)
birth_time = st.sidebar.time_input("Time of Birth")
birth_place = st.sidebar.text_input("Place of Birth", value="Mumbai, India")

# 3. Main Interface: Target Prediction Date
st.subheader("📅 Select Future Date for Prediction")

today = datetime.today().date()
max_future_date = today + timedelta(days=365 * 30)

target_date = st.date_input(
    "Choose any target date within the next 30 years:",
    value=today,
    min_value=today,
    max_value=max_future_date,
)

# 4. Planetary Cycle Helper Functions
def get_jupiter_theme(target_year, birth_year):
    # Jupiter completes a orbit roughly every 12 years
    cycle_years = (target_year - birth_year) % 12
    if cycle_years in [0, 4, 8]:
        return "Expansion, higher learning, and mentor alignment."
    elif cycle_years in [1, 5, 9]:
        return "Consolidation of gains, financial focus, and steady growth."
    else:
        return "Reflection, internal learning, and skill refinement."


def get_saturn_theme(target_year, birth_year):
    # Saturn completes an orbit roughly every 29.5 years
    cycle = (target_year - birth_year) % 30
    if cycle < 7:
        return "Foundation building: High discipline required; establishing career roots."
    elif cycle < 15:
        return "Action & Execution: Testing your abilities in real-world challenges."
    elif cycle < 22:
        return "Harvest & Maturity: Seeing outcomes of efforts made over the last decade."
    else:
        return "Restructuring: Clearing out old patterns to prepare for the next 30-year cycle."


# 5. Generate Prediction Trigger
if st.button("🔮 Calculate Planetary Energy & Prediction"):
    st.markdown("---")
    st.success(
        f"**Prediction Profile Generated for:** {target_date.strftime('%B %d, %Y')}"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Birth Place:** {birth_place}")
        st.info(f"**Birth Date:** {birth_date.strftime('%d-%m-%Y')}")
    with col2:
        st.info(f"**Target Year:** {target_date.year}")
        st.info(
            f"**Future Offset:** {target_date.year - today.year} years from today"
        )

    # Transit Analysis Engine Output
    st.subheader("🪐 Major Planetary Transits on This Date")

    j_theme = get_jupiter_theme(target_date.year, birth_date.year)
    s_theme = get_saturn_theme(target_date.year, birth_date.year)

    st.markdown(f"""
    * **Saturn Transits (Shani Phase):** {s_theme}
    * **Jupiter Transits (Guru Alignment):** {j_theme}
    * **General Energy Focus:** Balance disciplined execution with continuous learning. 
    """)

    st.subheader("📜 Predictive Guidance Summary")
    st.write(f"""
    During the week of **{target_date.strftime('%d %B %Y')}**, your primary growth vector centers on long-term sustainability rather than short-term shortcuts. 
    Focus on structured effort, keeping promises to yourself, and building skills that compound over time.
    """)
