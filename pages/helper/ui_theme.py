import streamlit as st

def inject_custom_theme():
    """Inject enterprise-grade Police Command Center UI styling."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

        :root {
            --primary: #1d4ed8;
            --primary-glow: #2563eb;
            --dark-obsidian: #090d16;
            --card-dark: #0f172a;
            --card-light: #ffffff;
            --success-emerald: #10b981;
            --danger-crimson: #ef4444;
            --warning-amber: #f59e0b;
        }

        html, body, [class*="css"], .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }

        /* Reduce top padding in main container */
        .stMainBlockContainer, div[data-testid="stMainBlockContainer"] {
            padding-top: 1.8rem !important;
            padding-bottom: 2rem !important;
        }

        /* Streamlit Header */
        header[data-testid="stHeader"] {
            background: linear-gradient(135deg, #090d16 0%, #1e3a8a 100%) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.15);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #090d16 0%, #0f172a 100%) !important;
            border-right: 1px solid #1e293b !important;
        }
        section[data-testid="stSidebar"] * {
            color: #f1f5f9 !important;
        }

        /* Command Ticker Header */
        .command-ticker {
            background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px;
            padding: 8px 18px;
            color: #60a5fa;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.2);
        }
        .command-ticker .ticker-pulse {
            width: 10px;
            height: 10px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 10px #10b981;
            margin-right: 8px;
        }

        /* Hero Banner */
        .portal-header {
            background: linear-gradient(135deg, #090d16 0%, #1e3a8a 50%, #1d4ed8 100%);
            padding: 2.2rem 2.5rem;
            border-radius: 18px;
            color: white;
            box-shadow: 0 12px 30px -5px rgba(15, 23, 42, 0.35);
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }
        .portal-header h1 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            margin: 0 0 0.4rem 0 !important;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .portal-header p {
            font-size: 1.05rem;
            color: #cbd5e1;
            margin: 0;
            max-width: 780px;
        }
        .portal-header .header-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: #93c5fd;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 0.8rem;
        }

        /* Cards */
        .custom-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 1.6rem 1.8rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
            margin-bottom: 1.5rem;
            transition: all 0.2s ease-in-out;
        }
        .custom-card:hover {
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.08);
            border-color: #cbd5e1;
        }

        /* Command Shortcuts Card */
        .shortcut-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            transition: all 0.25s ease-in-out;
        }
        .shortcut-card:hover {
            border-color: #3b82f6;
            box-shadow: 0 8px 22px rgba(59, 130, 246, 0.12);
            transform: translateY(-2px);
        }
        .shortcut-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            color: #0f172a;
        }
        .shortcut-desc {
            font-size: 0.85rem;
            color: #64748b;
            margin-top: 0.2rem;
        }

        /* Stat Card */
        .stat-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 1.3rem 1.5rem;
            border: 1px solid #e2e8f0;
            border-left: 5px solid #1d4ed8;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .stat-card.found { border-left-color: #10b981; }
        .stat-card.missing { border-left-color: #ef4444; }
        .stat-card.rate { border-left-color: #8b5cf6; }

        .stat-info .stat-label {
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #64748b;
            margin-bottom: 0.2rem;
        }
        .stat-info .stat-value {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.1;
        }
        .stat-icon { font-size: 2.3rem; }

        /* Status Pills */
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.3px;
        }
        .status-pill.found {
            background-color: #d1fae5;
            color: #047857;
            border: 1px solid #a7f3d0;
        }
        .status-pill.not-found {
            background-color: #fee2e2;
            color: #b91c1c;
            border: 1px solid #fca5a5;
        }

        /* Tracking Box */
        .tracking-box {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border: 1.5px solid #7dd3fc;
            border-radius: 14px;
            padding: 1.2rem 1.5rem;
            text-align: center;
            margin: 1rem 0;
        }
        .tracking-code {
            font-family: monospace;
            font-size: 1.6rem;
            font-weight: 800;
            color: #0369a1;
            letter-spacing: 2px;
            background: #ffffff;
            padding: 6px 18px;
            border-radius: 8px;
            border: 1px dashed #0284c7;
            display: inline-block;
            margin-top: 0.4rem;
        }

        /* Timeline Step */
        .timeline-step {
            display: flex;
            align-items: flex-start;
            gap: 15px;
            margin-bottom: 1.2rem;
            position: relative;
        }
        .timeline-step::before {
            content: '';
            position: absolute;
            left: 17px;
            top: 35px;
            bottom: -15px;
            width: 2px;
            background: #cbd5e1;
        }
        .timeline-step:last-child::before { display: none; }
        .timeline-icon {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #1d4ed8;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.95rem;
            z-index: 1;
        }
        .timeline-icon.completed { background: #10b981; }
        .timeline-icon.active { background: #f59e0b; }

        /* Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 0.6rem 1.3rem !important;
            box-shadow: 0 4px 12px rgba(29, 78, 216, 0.25) !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 18px rgba(29, 78, 216, 0.35) !important;
        }

        /* Login Card */
        .login-box {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 18px;
            padding: 2.2rem;
            box-shadow: 0 12px 32px rgba(15, 23, 42, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar_chatbot():
    """Render universal sidebar AVINASHI-AI assistant across all pages."""
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "assistant", "content": "👋 Welcome Officer Inika! I am **AVINASHI-AI**. Ask me anything about registered cases, location statistics, or facial mesh metrics!"}
        ]

    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🤖 AVINASHI-AI Assistant", expanded=False):
            st.caption("Police Command Intelligence Assistant")

            # Quick suggestion buttons (Instant Interactive Triggers)
            q1, q2 = st.columns(2)
            sb_selected = None
            if q1.button("📊 Total Cases", key="sb_btn_q1"):
                sb_selected = "How many total cases are registered?"
            elif q2.button("📍 Tiruppur", key="sb_btn_q2"):
                sb_selected = "Show cases in Tiruppur"

            if sb_selected:
                from pages.helper import chatbot_engine
                st.session_state["chat_history"].append({"role": "user", "content": sb_selected})
                user_name = st.session_state.get("username", "inika")
                response = chatbot_engine.query_avinashi_ai(sb_selected, current_user=user_name)
                st.session_state["chat_history"].append({"role": "assistant", "content": response})
                st.rerun()

            # Display last 4 messages in history
            for msg in st.session_state["chat_history"][-4:]:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**AVINASHI-AI:** {msg['content']}")

            # Form Input for query
            with st.form(key="sb_chat_form", clear_on_submit=True):
                sb_query = st.text_input(
                    "Ask AVINASHI-AI:",
                    placeholder="Type a question...",
                    label_visibility="collapsed"
                )
                submit_sb = st.form_submit_button("💬 Send Query", type="primary", use_container_width=True)

            if submit_sb and sb_query.strip():
                from pages.helper import chatbot_engine
                st.session_state["chat_history"].append({"role": "user", "content": sb_query})
                user_name = st.session_state.get("username", "inika")
                response = chatbot_engine.query_avinashi_ai(sb_query, current_user=user_name)
                st.session_state["chat_history"].append({"role": "assistant", "content": response})
                st.rerun()

def render_ticker():
    """Render live command ticker header bar."""
    st.markdown(
        """
        <div class="command-ticker">
            <div>
                <span class="ticker-pulse"></span>
                <span>POLICE COMMAND CENTER ACTIVE &nbsp;·&nbsp; AI LANDMARK MESH CORE ONLINE</span>
            </div>
            <div>STATUS: OPTIMAL &nbsp;|&nbsp; 468 3D VECTORS INDEXED</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_header(title: str, subtitle: str = "", badge: str = "OFFICER & PUBLIC PORTAL", icon: str = "🛡️"):
    """Render a unified high-end page header banner."""
    render_ticker()
    render_sidebar_chatbot()
    st.markdown(
        f"""
        <div class="portal-header">
            {f'<div class="header-badge">{badge}</div>' if badge else ''}
            <h1><span>{icon}</span> {title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_metric_card(title: str, value: str, icon: str = "📊", variant: str = "default"):
    """Render a custom visual stat card."""
    variant_class = variant if variant in ["found", "missing", "rate"] else ""
    st.markdown(
        f"""
        <div class="stat-card {variant_class}">
            <div class="stat-info">
                <div class="stat-label">{title}</div>
                <div class="stat-value">{value}</div>
            </div>
            <div class="stat-icon">{icon}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_status_badge(status: str) -> str:
    """Return HTML snippet for a status pill badge."""
    if status == "F" or status.lower() == "found":
        return '<span class="status-pill found">● FOUND / RESOLVED</span>'
    else:
        return '<span class="status-pill not-found">● SEARCHING / ACTIVE</span>'

def render_login_prompt(page_name: str = "this feature"):
    """Render a friendly login prompt card with a 1-click login button for restricted officer pages."""
    st.markdown(
        f"""
        <div class="custom-card" style="text-align: center; padding: 2.5rem 1.5rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔒</div>
            <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.4rem; font-weight: 700; color: #0f172a; margin: 0;">
                Officer Sign-In Required
            </h3>
            <p style="color: #64748b; font-size: 0.95rem; margin-top: 0.4rem; max-width: 500px; margin-left: auto; margin-right: auto;">
                You are viewing <strong>{page_name}</strong>. Please sign in as an officer or click below for instant 1-Click Officer Sign-In access.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("⚡ Instant 1-Click Officer Sign-In", key=f"quick_login_{page_name}", type="primary", use_container_width=True):
            st.session_state["authentication_status"] = True
            st.session_state["username"] = "inika"
            st.session_state["user"] = "inika"
            st.session_state["role"] = "Admin"
            st.session_state["login_status"] = True
            st.rerun()

