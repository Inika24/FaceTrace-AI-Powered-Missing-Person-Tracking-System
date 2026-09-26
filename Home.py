import os
import yaml
import base64
import streamlit as st
from yaml import SafeLoader
import streamlit_authenticator as stauth

from pages.helper import db_queries
from pages.helper import ui_theme

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
                <div style="margin-top: 0.8rem;">
                    <span style="background: #e0f2fe; color: #0369a1; padding: 5px 15px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; border: 1px solid #bae6fd;">
                        ⚡ AI Facial Mesh 468 Landmark Core & CCTV Scanner
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Demo Sign-In Card & Instant Login
        st.markdown(
            """
            <div class="login-box" style="margin-bottom: 1.5rem;">
                <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.2rem; font-weight: 700; color: #0f172a; margin-top: 0; text-align: center;">
                    👮 Station Officer Portal Sign-In
                </h3>
                <div style="background: #f1f5f9; border-radius: 10px; padding: 0.8rem; margin: 0.8rem 0; font-size: 0.88rem; color: #334155; text-align: center;">
                    🔑 <strong>Demo Station Credentials:</strong><br>
                    Username: <code style="color: #1d4ed8; font-weight: 700;">inika</code> &nbsp;|&nbsp; 
                    Password: <code style="color: #1d4ed8; font-weight: 700;">abc</code>
                </div>
            """,
            unsafe_allow_html=True,
        )

        demo_login_btn = st.button("⚡ Instant 1-Click Officer Sign-In (Demo Access)", key="home_demo_btn", type="primary")
        if demo_login_btn:
            st.session_state["authentication_status"] = True
            st.session_state["username"] = "inika"
            st.session_state["login_status"] = True
            st.rerun()

        st.markdown("<div style='text-align:center; color:#94a3b8; font-size:0.85rem; margin:0.8rem 0;'>or sign in below</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Perform authenticator login widget only when not authenticated
if not st.session_state.get("authentication_status"):
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

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Interactive Cases Map Section ─────────────────────────────────────────
    st.markdown(
        """
        <div style="background: #ffffff; border-radius: 16px; padding: 1.5rem; border: 1px solid #e2e8f0; box-shadow: 0 4px 14px rgba(0,0,0,0.03);">
            <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.3rem; font-weight: 700; color: #0f172a; margin-top: 0;">
                📍 Nationwide Case Density Map
            </h3>
        """,
        unsafe_allow_html=True,
    )

    try:
        import folium
        from streamlit_folium import st_folium

        CITY_COORDS = {
            "Delhi": (28.6139, 77.2090),
            "New Delhi": (28.6139, 77.2090),
            "Mumbai": (19.0760, 72.8777),
            "Bengaluru": (12.9716, 77.5946),
            "Bangalore": (12.9716, 77.5946),
            "Hyderabad": (17.3850, 78.4867),
            "Chennai": (13.0827, 80.2707),
            "Kolkata": (22.5726, 88.3639),
            "Pune": (18.5204, 73.8567),
            "Ahmedabad": (23.0225, 72.5714),
            "Jaipur": (26.9124, 75.7873),
            "Lucknow": (26.8467, 80.9462),
            "Kanpur": (26.4499, 80.3319),
            "Nagpur": (21.1458, 79.0882),
            "Indore": (22.7196, 75.8577),
            "Bhopal": (23.2599, 77.4126),
            "Visakhapatnam": (17.6868, 83.2185),
            "Patna": (25.5941, 85.1376),
            "Vadodara": (22.3072, 73.1812),
            "Surat": (21.1702, 72.8311),
            "Noida": (28.5355, 77.3910),
            "Gurgaon": (28.4595, 77.0266),
            "Gurugram": (28.4595, 77.0266),
            "Chandigarh": (30.7333, 76.7794),
            "Coimbatore": (11.0168, 76.9558),
            "Kochi": (9.9312, 76.2673),
            "Agra": (27.1767, 78.0081),
            "Varanasi": (25.3176, 82.9739),
            "Meerut": (28.9845, 77.7064),
            "Raipur": (21.2514, 81.6296),
            "Ranchi": (23.3441, 85.3096),
            "Guwahati": (26.1445, 91.7362),
            "Jodhpur": (26.2389, 73.0243),
            "Amritsar": (31.6340, 74.8723),
            "Faridabad": (28.4089, 77.3178),
            "Allahabad": (25.4358, 81.8463),
            "Prayagraj": (25.4358, 81.8463),
            "Mathura": (27.4924, 77.6737),
            "Bareilly": (28.3670, 79.4304),
            "Aligarh": (27.8974, 78.0880),
            "Moradabad": (28.8386, 78.7733),
            "Saharanpur": (29.9680, 77.5460),
            "Gorakhpur": (26.7606, 83.3732),
            "Firozabad": (27.1591, 78.3957),
            "Jhansi": (25.4484, 78.5685),
            "Ghaziabad": (28.6692, 77.4538),
            "Ludhiana": (30.9010, 75.8573),
            "Jalandhar": (31.3260, 75.5762),
            "Dehradun": (30.3165, 78.0322),
            "Haridwar": (29.9457, 78.1642),
            "Rishikesh": (30.0869, 78.2676),
            "Shimla": (31.1048, 77.1734),
            "Bathinda": (30.2110, 74.9455),
            "Unknown": (20.5937, 78.9629),
        }

        counts = db_queries.get_case_counts_by_city()

        if not counts:
            st.info("ℹ️ No cases with city location data available yet. Register a new case to populate map pins.")
        else:
            m = folium.Map(
                location=[20.5937, 78.9629], zoom_start=5, tiles="OpenStreetMap"
            )

            for city, data in counts.items():
                total = data["found"] + data["not_found"]
                coords = CITY_COORDS.get(city)
                if coords is None:
                    for key, val in CITY_COORDS.items():
                        if key.lower() == city.lower():
                            coords = val
                            break
                if coords is None:
                    continue

                color = "#ef4444" if data["not_found"] > 0 else "#10b981"
                tooltip = (
                    f"<b>{city}</b><br>"
                    f"Total Cases: {total}<br>"
                    f"Active Missing: {data['not_found']}<br>"
                    f"Resolved/Found: {data['found']}"
                )
                folium.CircleMarker(
                    location=coords,
                    radius=max(8, min(35, total * 5)),
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.6,
                    tooltip=folium.Tooltip(tooltip),
                ).add_to(m)

            st_folium(m, width="100%", height=440, returned_objects=[])

            st.markdown(
                """
                <div style="font-size: 0.85rem; color: #64748b; margin-top: 10px; display: flex; gap: 15px; align-items: center;">
                    <span><strong style="color: #ef4444;">🔴 Has Unresolved Cases</strong></span>
                    <span><strong style="color: #10b981;">🟢 All Cases Resolved</strong></span>
                    <span><em>Circle size reflects total case volume</em></span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except ImportError:
        st.info("ℹ️ Install `folium` and `streamlit-folium` to render the GIS map.")

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.get("authentication_status") == False:
    st.error("❌ Invalid Username or Password. Please try again.")
elif st.session_state.get("authentication_status") is None:
    st.session_state["login_status"] = False
