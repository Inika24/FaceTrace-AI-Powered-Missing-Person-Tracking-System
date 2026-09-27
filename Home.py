import os
import yaml
import base64
import streamlit as st
from yaml import SafeLoader
import streamlit_authenticator as stauth

from pages.helper import db_queries
from pages.helper import ui_theme
from pages.helper import chatbot_engine

st.set_page_config(
    page_title="Missing Person AI Identification & Command Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Global Command Center Theme
ui_theme.inject_custom_theme()

# Initialise DB once at startup
db_queries.create_db()

if "login_status" not in st.session_state:
    st.session_state["login_status"] = False

config = None
if os.path.exists("login_config.yml"):
    try:
        with open("login_config.yml") as file:
            config = yaml.load(file, Loader=SafeLoader)
    except Exception:
        pass

if not config and hasattr(st, "secrets") and "credentials" in st.secrets:
    try:
        config = dict(st.secrets)
    except Exception:
        pass

if not config:
    config = {
        "credentials": {
            "usernames": {
                "inika": {
                    "email": "inikab@gmail.com",
                    "name": "Inika B",
                    "city": "Tiruppur",
                    "area": "Avinashi",
                    "role": "Admin",
                    "password": "$2b$12$ByZbwxrcvCXVLQO4zjI95OteXToaBiwWDqujsHiKfeGzionz0VqAG"
                }
            }
        },
        "cookie": {
            "expiry_days": 1,
            "key": "a8f3d2e1b9c7f4a0e5d6c3b2a1f8e7d4c9b0a3f2e1d8c7b6a5f4e3d2c1b0a9",
            "name": "random_cookie_name"
        },
        "preauthorized": {"emails": ["inikab@gmail.com"]}
    }

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# ── Login & Live Case Tracking Section (When Not Logged In) ───────────────────
if not st.session_state.get("authentication_status"):
    col_left, col_center, col_right = st.columns([1, 2.2, 1])

    with col_center:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 1.5rem; margin-bottom: 1.5rem;">
                <div style="font-size: 3.5rem; margin-bottom: 0.3rem;">🛡️</div>
                <h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 0;">
                    Missing Person AI Portal & Command Network
                </h1>
                <p style="color: #64748b; font-size: 1.05rem; margin-top: 0.4rem;">
                    Law Enforcement Officer & Public Intelligence Network
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Sign-In Card
        st.markdown(
            """
            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 18px; padding: 1.5rem; box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08); text-align: center; margin-bottom: 1.2rem;">
                <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.25rem; font-weight: 700; color: #0f172a; margin: 0;">
                    👮 Station Officer Portal Sign-In
                </h3>
                <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.3rem; margin-bottom: 0;">
                    Authorized Station Officers & Command Administrators
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Instant 1-Click Officer Sign-In Button
        if st.button("⚡ Instant 1-Click Officer Sign-In", type="primary", use_container_width=True, key="home_1click_signin_btn"):
            st.session_state["authentication_status"] = True
            st.session_state["username"] = "inika"
            st.session_state["user"] = "inika"
            st.session_state["name"] = "Inika B"
            st.session_state["role"] = "Admin"
            st.session_state["login_status"] = True
            st.rerun()

        st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.85rem; margin: 0.8rem 0 0.4rem 0;'>— OR ENTER STATION CREDENTIALS —</div>", unsafe_allow_html=True)

        try:
            authenticator.login(location="main")
        except Exception:
            pass

# ── Post-Login Officer Dashboard ──────────────────────────────────────────────
if st.session_state.get("authentication_status"):
    st.session_state["login_status"] = True
    user_info = config["credentials"]["usernames"][st.session_state["username"]]
    st.session_state["user"] = st.session_state["username"]

    role = user_info.get("role", "Officer")
    st.session_state["role"] = role

    # Sidebar Officer Profile Card
    with st.sidebar:
        st.markdown(
            f"""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1.5rem;">
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">LOGGED IN AS</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; margin: 0.2rem 0;">👮 {user_info['name']}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1;">📍 {user_info['area']}, {user_info['city']}</div>
                <div style="margin-top: 0.6rem;">
                    <span style="background: {'#ef4444' if role.lower() == 'admin' else '#10b981'}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">
                        {role.upper()}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        authenticator.logout("🔒 Sign Out", "sidebar")
        st.markdown("---")
        st.caption("Missing Person AI Portal v3.0 • Command Build")

    # Top Page Header
    ui_theme.render_header(
        title=f"Welcome, Officer {user_info['name']}",
        subtitle=f"Station Area: {user_info['area']}, {user_info['city']} • AI Landmark Engine: Active",
        badge=f"{role.upper()} COMMAND CENTER",
        icon="🛡️"
    )

    # Calculate Case Metrics
    found_cases = db_queries.get_registered_cases_count(st.session_state["user"], "F")
    non_found_cases = db_queries.get_registered_cases_count(st.session_state["user"], "NF")
    
    total_count = len(found_cases) + len(non_found_cases)
    found_count = len(found_cases)
    missing_count = len(non_found_cases)
    rate = f"{(found_count / total_count * 100):.1f}%" if total_count > 0 else "0%"

    # Stat Cards Grid
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        ui_theme.render_metric_card("Total Registered Cases", str(total_count), icon="📁", variant="default")
    with m2:
        ui_theme.render_metric_card("Resolved / Found", str(found_count), icon="✅", variant="found")
    with m3:
        ui_theme.render_metric_card("Active Missing", str(missing_count), icon="🚨", variant="missing")
    with m4:
        ui_theme.render_metric_card("Resolution Rate", rate, icon="📈", variant="rate")

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Shortcuts Banner (Spacious 2x2 Layout)
    st.subheader("⚡ Command Shortcuts & Advanced Modules")
    sc_col1, sc_col2 = st.columns(2, gap="medium")

    with sc_col1:
        st.markdown(
            """
            <div class="shortcut-card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="shortcut-icon" style="margin: 0; font-size: 2.2rem;">⏳</div>
                    <div>
                        <div class="shortcut-title" style="font-size: 1.05rem;">AI Age Progression Studio</div>
                        <div class="shortcut-desc">+5 / +10 / +15Y predictive face growth & landmark scan</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="shortcut-card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="shortcut-icon" style="margin: 0; font-size: 2.2rem;">🔍</div>
                    <div>
                        <div class="shortcut-title" style="font-size: 1.05rem;">Live Case Tracker</div>
                        <div class="shortcut-desc">Track status by Aadhaar, Mobile Number, Name, or Case ID</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with sc_col2:
        st.markdown(
            """
            <div class="shortcut-card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="shortcut-icon" style="margin: 0; font-size: 2.2rem;">📹</div>
                    <div>
                        <div class="shortcut-title" style="font-size: 1.05rem;">CCTV Crowd Video Scanner</div>
                        <div class="shortcut-desc">Real-time crowd video frame scanning & bounding box alerts</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="shortcut-card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="shortcut-icon" style="margin: 0; font-size: 2.2rem;">🤖</div>
                    <div>
                        <div class="shortcut-title" style="font-size: 1.05rem;">AI Matching Engine</div>
                        <div class="shortcut-desc">Run KNN 468 3D landmark mesh comparison & email alerts</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── AVINASHI-AI Conversational Assistant Module ─────────────────────────────
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #090d16 0%, #1e3a8a 100%); padding: 1.2rem 1.5rem; border-radius: 12px; color: white; margin-bottom: 1.2rem;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #93c5fd; text-transform: uppercase; letter-spacing: 0.5px;">CONVERSATIONAL AI ENGINE</div>
            <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.35rem; font-weight: 800; color: #ffffff; margin: 0.2rem 0;">
                🤖 AVINASHI-AI — Command Intelligence Assistant
            </h3>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0;">
                Ask natural language questions about missing records, city case density, birthmark features, or AI algorithms.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "assistant", "content": "👋 Welcome Officer Inika! I am **AVINASHI-AI**. Ask me anything about registered cases, location statistics, or facial mesh metrics!"}
        ]

    # Quick Suggestion Chips (Instant Interactive Triggers)
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    selected_query = None
    if q_col1.button("📊 Total Cases Count", key="btn_q1"):
        selected_query = "How many total cases are registered?"
    elif q_col2.button("📍 Cases in Tiruppur", key="btn_q2"):
        selected_query = "Show cases in Tiruppur"
    elif q_col3.button("🔍 Birthmark Search", key="btn_q3"):
        selected_query = "Find cases with birthmark on chin"
    elif q_col4.button("🧠 Explain AI Mesh", key="btn_q4"):
        selected_query = "Explain 468 landmark mesh algorithm"

    if selected_query:
        st.session_state["chat_history"].append({"role": "user", "content": selected_query})
        response = chatbot_engine.query_avinashi_ai(selected_query, current_user=st.session_state.get("user", "inika"))
        st.session_state["chat_history"].append({"role": "assistant", "content": response})
        st.rerun()

    # Chat message history
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Form Input for query
    with st.form(key="sentinel_chat_form", clear_on_submit=True):
        chat_query = st.text_input(
            "Type your question for AVINASHI-AI below:",
            placeholder="e.g. Hi! or How many cases in Tiruppur? or Search birthmark..."
        )
        submit_chat = st.form_submit_button("💬 Send Query to AVINASHI-AI", type="primary")

    if submit_chat and chat_query.strip():
        st.session_state["chat_history"].append({"role": "user", "content": chat_query})
        response = chatbot_engine.query_avinashi_ai(chat_query, current_user=st.session_state.get("user", "inika"))
        st.session_state["chat_history"].append({"role": "assistant", "content": response})
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Interactive Cases Map Section ─────────────────────────────────────────
    st.subheader("📍 Geographic Case Density Map (City / State / Country)")
    counts = db_queries.get_case_counts_by_city()

    if not counts:
        st.info("ℹ️ No cases with location data available yet. Register a new case to populate map pins.")
    else:
        from pages.helper import geo_utils
        geo_utils.render_english_map(counts, height=450)

        st.markdown(
            """
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 10px; display: flex; gap: 15px; align-items: center; margin-bottom: 2rem;">
                <span><strong style="color: #ef4444;">🔴 Has Unresolved Cases</strong></span>
                <span><strong style="color: #10b981;">🟢 All Cases Resolved</strong></span>
                <span><em>Circle size reflects total case volume</em></span>
            </div>
            """,
            unsafe_allow_html=True,
        )

elif st.session_state.get("authentication_status") == False:
    st.error("❌ Invalid Username or Password. Please try again.")
elif st.session_state.get("authentication_status") is None:
    st.session_state["login_status"] = False
