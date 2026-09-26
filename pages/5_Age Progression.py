import streamlit as st
import numpy as np
from PIL import Image

from sqlmodel import Session, select
from pages.helper.db_queries import engine
from pages.helper.data_models import RegisteredCases
from pages.helper import db_queries, match_algo
from pages.helper.utils import image_obj_to_numpy, draw_face_boxes, detect_all_faces
from pages.helper.age_simulator import simulate_age_progression
from pages.helper import ui_theme

st.set_page_config(
    page_title="Age Progression Studio • Missing Person AI",
    page_icon="⏳",
    layout="wide"
)

ui_theme.inject_custom_theme()

if "login_status" not in st.session_state or not st.session_state["login_status"]:
    ui_theme.render_header(
        title="AI Age-Progression Studio",
        subtitle="Predictive facial growth simulation for long-term missing cases",
        badge="GENERATIVE AI ENGINE",
        icon="⏳"
    )
    ui_theme.render_login_prompt("AI Age Progression Studio")
    st.stop()

user = st.session_state.user

ui_theme.render_header(
    title="AI Facial Age-Progression Studio",
    subtitle="Predictive aging transform (+5, +10, +15 Years) & aged 3D landmark vector matching for long-term missing persons",
    badge="GENERATIVE AI RECOVERY ENGINE",
    icon="⏳"
)

# Input Mode Card
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.markdown("### 👤 Select Target Case or Upload Photo")

source_mode = st.radio(
    "Select Source Photo",
    options=["📋 Select from Active Registered Cases", "📸 Upload Custom Child / Person Photo"],
    horizontal=True,
    key="age_source_mode"
)

target_img_np = None
case_id = None
person_name = "Target Subject"

if "Registered" in source_mode:
    active_cases = db_queries.get_not_confirmed_registered_cases(user)
    if not active_cases:
        st.info("ℹ️ No active missing cases registered yet. Upload a photo directly below or register a case first.")
    else:
        case_map = {f"{c.name} (Age: {c.age}, Last Seen: {c.last_seen}) — ID: {c.id[:8]}...": c for c in active_cases}
        chosen = st.selectbox("Select Missing Person Record", list(case_map.keys()))
        selected_case = case_map[chosen]
        case_id = selected_case.id
        person_name = selected_case.name

        img_path = f"./resources/{case_id}.jpg"
        try:
            pil_img = Image.open(img_path)
            target_img_np = np.array(pil_img)
        except Exception:
            st.error("Could not load original case image from disk.")
else:
    up_file = st.file_uploader("Upload Person Photo", type=["jpg", "jpeg", "png"], key="age_up_file")
    if up_file:
        target_img_np = image_obj_to_numpy(up_file)
        person_name = "Uploaded Subject"

st.markdown("</div>", unsafe_allow_html=True)

if target_img_np is not None:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown(f"### ⚙️ Predictive Aging Projection Settings — **{person_name}**")

    c1, c2 = st.columns([2.5, 1], gap="medium")

    with c1:
        years_to_add = st.select_slider(
            "Select Years to Add (+5Y to +20Y)",
            options=[5, 10, 15, 20],
            value=10,
            format_func=lambda x: f"+{x} Years Predictive Aging"
        )

    with c2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        gen_btn = st.button("✨ Run AI Age Simulation", type="primary", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Execute simulation on button click or if stored in session state
    if gen_btn:
        st.session_state["run_age_sim"] = True
        st.session_state["sim_years"] = years_to_add

    if st.session_state.get("run_age_sim"):
        current_years = st.session_state.get("sim_years", years_to_add)
        with st.spinner(f"✨ Generating +{current_years}-year facial progression & extrapolating landmark mesh..."):
            aged_np, aged_landmarks = simulate_age_progression(target_img_np, years=current_years)

        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown(f"### 📸 Visual Comparison: Original Photo vs +{current_years} Years Projection")

        img_col1, img_col2 = st.columns(2, gap="large")

        with img_col1:
            st.image(target_img_np, use_container_width=True, caption=f"Original Case Photo ({person_name})")

        with img_col2:
            st.image(aged_np, use_container_width=True, caption=f"AI Predictive Aging Projection (+{current_years} Years)")

        # AI Transformation Analytics Breakdown
        st.markdown(
            f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem 1.2rem; margin-top: 1.2rem; font-size: 0.88rem; color: #334155;">
                <div style="font-weight: 700; color: #1e3a8a; font-size: 0.95rem; margin-bottom: 0.5rem;">
                    🧬 Generative Aging Transformation Breakdown (+{current_years} Years):
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center;">
                    <div style="background: #ffffff; padding: 0.6rem; border-radius: 8px; border: 1px solid #cbd5e1;">
                        <div style="font-size: 0.75rem; color: #64748b;">wrinkle Intensity</div>
                        <div style="font-weight: 800; color: #0f172a;">+{(current_years/20.0 * 2.2):.1f}x Deep Fold</div>
                    </div>
                    <div style="background: #ffffff; padding: 0.6rem; border-radius: 8px; border: 1px solid #cbd5e1;">
                        <div style="font-size: 0.75rem; color: #64748b;">Hair Silver Shift</div>
                        <div style="font-weight: 800; color: #0f172a;">+{int((current_years/20.0 * 75))}% Silver</div>
                    </div>
                    <div style="background: #ffffff; padding: 0.6rem; border-radius: 8px; border: 1px solid #cbd5e1;">
                        <div style="font-size: 0.75rem; color: #64748b;">Jaw/Cheek Sag</div>
                        <div style="font-weight: 800; color: #0f172a;">+{(current_years * 0.4):.1f}% Tissue Sag</div>
                    </div>
                    <div style="background: #ffffff; padding: 0.6rem; border-radius: 8px; border: 1px solid #cbd5e1;">
                        <div style="font-size: 0.75rem; color: #64748b;">3D Vector Mesh</div>
                        <div style="font-weight: 800; color: #10b981;">468 Points Shifted</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Landmark Vector Rescan Trigger
        if aged_landmarks:
            st.markdown("---")
            st.markdown("#### 🔍 Database Cross-Match with Aged Vector")
            st.caption("Cross-reference projected +aged landmark coordinates against all public sighting uploads.")
            
            rescan_btn = st.button(f"🔎 Execute AI Scan Using +{current_years}Y Aged Vector", type="primary")
            if rescan_btn:
                public_cases = db_queries.fetch_public_cases(True, "NF")
                if not public_cases:
                    st.info("ℹ️ No public sighting reports currently registered in database.")
                else:
                    st.success(f"Scanning {len(public_cases)} public sighting report(s)...")
                    found = 0
                    for pub_id, pub_mesh_str in public_cases:
                        import json
                        pub_landmarks = json.loads(pub_mesh_str)
                        dist = match_algo.calculate_distance(aged_landmarks, pub_landmarks)
                        if dist <= 3.0:
                            conf = max(0.0, min(100.0, (1.0 - dist / 3.0) * 100))
                            st.success(f"🎉 **Match Flagged!** Public Sighting ID `{pub_id[:8]}` matches +{current_years}Y aged vector with **{conf:.1f}% confidence!**")
                            found += 1
                    if found == 0:
                        st.info(f"Scan complete. No public sighting reports matched the +{current_years}Y aged vector threshold.")

        st.markdown("</div>", unsafe_allow_html=True)
