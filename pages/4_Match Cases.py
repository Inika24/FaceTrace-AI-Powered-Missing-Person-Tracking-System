import streamlit as st

from pages.helper import db_queries, match_algo, train_model
from pages.helper import emailer
from pages.helper import ui_theme

st.set_page_config(
    page_title="AI Match Cases • Missing Person AI",
    page_icon="🤖",
    layout="wide"
)

ui_theme.inject_custom_theme()

DISTANCE_THRESHOLD = 3.0


def confidence_from_distance(distance: float) -> float:
    """Convert a KNN distance to a 0–100 confidence percentage."""
    return max(0.0, min(100.0, (1.0 - distance / DISTANCE_THRESHOLD) * 100))


def case_viewer(registered_case_id: str, public_case_id: str, confidence: float = None):
    try:
        case_details = db_queries.get_registered_case_detail(registered_case_id)[0]
        public_details = db_queries.get_public_case_detail(public_case_id)

        db_queries.update_found_status(registered_case_id, public_case_id)

        st.markdown(
            f"""
            <div class="custom-card" style="border-left: 6px solid #10b981; background: #ffffff;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.3rem; font-weight: 800; color: #065f46;">
                        🎉 High Confidence Facial Match Found
                    </div>
                    <div style="background: #d1fae5; color: #047857; padding: 4px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                        STATUS: RESOLVED (FOUND)
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        reg_col, match_metric_col, pub_col = st.columns([2, 1.5, 2])

        with reg_col:
            st.markdown("##### 👤 Registered Missing Person")
            try:
                st.image(
                    "./resources/" + registered_case_id + ".jpg",
                    use_container_width=True,
                    caption=f"Tracking ID: {registered_case_id}"
                )
            except Exception:
                st.caption("No Image Available")

            labels = ["Name", "Complainant Phone", "Age", "Last Seen", "Birth Marks"]
            display_values = [
                case_details[0],  # name
                case_details[1],  # complainant_mobile
                case_details[3],  # age
                case_details[4],  # last_seen
                case_details[5],  # birth_marks
            ]
            for text, val in zip(labels, display_values):
                st.write(f"**{text}:** {val}")

        with match_metric_col:
            st.markdown("<br>", unsafe_allow_html=True)
            if confidence is not None:
                st.markdown(
                    f"""
                    <div style="text-align: center; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 1rem;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #166534; text-transform: uppercase; letter-spacing: 0.5px;">MATCH CONFIDENCE</div>
                        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.2rem; font-weight: 800; color: #15803d; margin: 0.2rem 0;">
                            {confidence:.1f}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(confidence / 100)

        with pub_col:
            st.markdown("##### 📢 Matched Public Sighting Report")
            try:
                st.image(
                    "./resources/" + public_case_id + ".jpg",
                    use_container_width=True,
                    caption=f"Sighting ID: {public_case_id}"
                )
            except Exception:
                st.caption("No Image Available")

            if public_details and len(public_details) > 0:
                p_row = public_details[0]
                st.write(f"**Location Seen:** {p_row[0]}")
                st.write(f"**Reported By:** {p_row[1]}")
                st.write(f"**Reporter Mobile:** {p_row[2]}")
                st.write(f"**Sighting Birthmarks:** {p_row[3]}")

        sent = emailer.send_match_notification(registered_case_id, case_details)
        if sent:
            st.info(f"📧 Automated dispatch: Notification email successfully sent to complainant at **{case_details[2]}**")

        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        import traceback
        traceback.print_exc()
        st.error(f"❌ Error processing match verification: {str(e)}")


# ── Page Logic ───────────────────────────────────────────────────────────────

if "login_status" not in st.session_state or not st.session_state["login_status"]:
    ui_theme.render_header(
        title="AI Facial Landmark Matching Core",
        subtitle="Train KNN vector classifier on MediaPipe 468 3D landmark embeddings and perform automated cross-verification",
        badge="AUTOMATED RECOGNITION ENGINE",
        icon="🤖"
    )
    ui_theme.render_login_prompt("AI Matching Engine")
    st.stop()

user = st.session_state.user
is_admin = st.session_state.get("role", "").lower() == "admin"

ui_theme.render_header(
    title="AI Facial Landmark Matching Core",
    subtitle="Train KNN vector classifier on MediaPipe 468 3D landmark embeddings and perform automated cross-verification",
    badge="AUTOMATED RECOGNITION ENGINE",
    icon="🤖"
)

if not is_admin:
    st.markdown(
        """
        <div class="custom-card" style="text-align: center; padding: 2.5rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔒</div>
            <h3 style="color: #0f172a; margin-bottom: 0.3rem;">Administrator Privilege Required</h3>
            <p style="color: #64748b;">Only authorized Station Administrators can execute the KNN facial recognition matching pipeline.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="custom-card">
            <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.2rem; font-weight: 700; color: #0f172a; margin-top: 0;">
                ⚡ Execute Facial Recognition Matching Scan
            </h3>
            <p style="color: #64748b; font-size: 0.92rem;">
                Click the button below to train the KNN spatial model on all registered complaints and calculate L2 Euclidean landmark distances against public sighting uploads.
            </p>
        """,
        unsafe_allow_html=True,
    )

    refresh_bt = st.button("🔄 Execute AI Facial Scan Now")
    st.markdown("</div>", unsafe_allow_html=True)

    if refresh_bt:
        with st.spinner("🤖 Training KNN landmark model & scanning database for matches..."):
            result = train_model.train(user)
            matched_ids = match_algo.match()

            if matched_ids["status"]:
                if not matched_ids["result"]:
                    st.info("ℹ️ **Scan Complete:** No new facial matches detected at current distance threshold (3.0).")
                else:
                    st.success(f"🎉 **Scan Complete:** Found {len(matched_ids['result'])} matching case pair(s)!")
                    for matched_id, submitted_cases in matched_ids["result"].items():
                        for submitted_case in submitted_cases:
                            if isinstance(submitted_case, tuple):
                                submitted_case_id, distance = submitted_case
                                conf = confidence_from_distance(distance)
                            else:
                                submitted_case_id = submitted_case
                                conf = None

                            case_viewer(matched_id, submitted_case_id, conf)
            else:
                st.info("ℹ️ **Scan Complete:** No new facial matches found.")
