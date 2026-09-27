import streamlit as st
import pandas as pd

from sqlmodel import Session, select
from pages.helper.db_queries import engine
from pages.helper.data_models import RegisteredCases
from pages.helper import db_queries
from pages.helper import ui_theme

st.set_page_config(
    page_title="Track Missing Person Case • AI Portal",
    page_icon="🔍",
    layout="wide"
)

ui_theme.inject_custom_theme()

ui_theme.render_header(
    title="Live Missing Person Case Tracker",
    subtitle="Track case status, view AI match timeline, location map, and official sighting updates using Aadhaar, Phone, Name, or Case ID",
    badge="PUBLIC & OFFICER CASE SEARCH",
    icon="🔍"
)

# Search Input Card
s_col1, s_col2 = st.columns([4, 1])

with s_col1:
    search_query = st.text_input(
        "Enter Aadhaar Number, Complainant Phone, Person Name, or Case ID to Track",
        placeholder="e.g. Type Aadhaar (12 digits), Mobile (10 digits), Name (e.g. Inika), or Case ID...",
        key="tracker_input"
    )

with s_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("🔎 Track Case")

if not search_query.strip():
    st.markdown(
        """
        <div class="custom-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📋</div>
            <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.25rem; font-weight: 700; color: #0f172a;">
                Multi-Identifier Case Search
            </h3>
            <p style="color: #64748b; font-size: 0.92rem; max-width: 650px; margin: 0.4rem auto 0 auto;">
                You don't need to memorize a long Case ID. Enter your <strong>Aadhaar Number</strong>, <strong>Complainant Phone Number</strong>, <strong>Missing Person Name</strong>, or <strong>Case ID</strong> above to track live status and AI match updates.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    query = search_query.strip().lower()
    matched_cases = []

    with Session(engine) as session:
        all_cases = session.exec(select(RegisteredCases)).all()
        for c in all_cases:
            if (
                query == c.id.lower()
                or query in c.name.lower()
                or (c.adhaar_card and query in c.adhaar_card.lower())
                or (c.complainant_mobile and query in c.complainant_mobile.lower())
                or (c.complainant_name and query in c.complainant_name.lower())
            ):
                matched_cases.append(c)

    if not matched_cases:
        st.error(f"❌ No record found matching **'{search_query}'**. Please verify the Aadhaar Number, Phone Number, Name, or Case ID.")
    else:
        st.success(f"✅ Found {len(matched_cases)} record(s) matching **'{search_query}'**:")

        for case_obj in matched_cases:
            case_id = case_obj.id
            status_pill = ui_theme.render_status_badge(case_obj.status)

            st.markdown(
                f"""
                <div class="custom-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                        <div>
                            <h2 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.4rem; font-weight: 800; color: #0f172a; margin: 0;">
                                👤 {case_obj.name}
                            </h2>
                            <div style="font-size: 0.88rem; color: #64748b; margin-top: 3px;">
                                📍 <strong>Last Seen:</strong> {case_obj.last_seen} ({case_obj.city or 'N/A'}) &nbsp;·&nbsp; 
                                🎂 <strong>Age:</strong> {case_obj.age or 'N/A'}
                            </div>
                        </div>
                        <div>{status_pill}</div>
                    </div>
                """,
                unsafe_allow_html=True,
            )

            # Case Tracking Code Banner
            st.markdown(
                f"""
                <div class="tracking-box">
                    <div style="font-size: 0.82rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.5px;">
                        CASE TRACKING ID & IDENTIFIERS
                    </div>
                    <div class="tracking-code">{case_id}</div>
                    <div style="font-size: 0.85rem; color: #0369a1; margin-top: 0.5rem;">
                        Aadhaar: <strong>{case_obj.adhaar_card or 'N/A'}</strong> &nbsp;|&nbsp; 
                        Complainant Mobile: <strong>{case_obj.complainant_mobile or 'N/A'}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            img_col, details_col, timeline_col = st.columns([1, 1.8, 2], gap="medium")

            with img_col:
                st.markdown("##### 📸 Person Photograph")
                try:
                    st.image(
                        "./resources/" + str(case_id) + ".jpg",
                        use_container_width=True,
                        caption=f"Indexed Image for {case_obj.name}"
                    )
                except Exception:
                    st.markdown(
                        """
                        <div style="background: #f1f5f9; border-radius: 12px; height: 160px; display: flex; align-items: center; justify-content: center; color: #94a3b8;">
                            No Image Found
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            with details_col:
                st.markdown("##### 📋 Case Record Details")
                st.markdown(
                    f"""
                    <div style="font-size: 0.9rem; color: #334155; line-height: 1.7;">
                        <div><strong>Father's Name:</strong> {case_obj.father_name or 'N/A'}</div>
                        <div><strong>Aadhaar Card:</strong> {case_obj.adhaar_card or 'N/A'}</div>
                        <div><strong>Distinguishing Marks:</strong> {case_obj.birth_marks or 'None'}</div>
                        <div><strong>Complainant Contact:</strong> {case_obj.complainant_name} ({case_obj.complainant_mobile})</div>
                        <div><strong>Date Registered:</strong> {str(case_obj.submitted_on)[:16]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with timeline_col:
                st.markdown("##### ⏱️ Case Tracking Timeline")
                is_found = (case_obj.status == "F")

                st.markdown(
                    f"""
                    <div style="padding: 0.5rem 0;">
                        <div class="timeline-step">
                            <div class="timeline-icon completed">✓</div>
                            <div>
                                <div style="font-weight: 700; font-size: 0.9rem; color: #0f172a;">1. Complaint Registered & AI Facial Indexing</div>
                                <div style="font-size: 0.8rem; color: #64748b;">468 3D landmark points extracted and saved</div>
                            </div>
                        </div>

                        <div class="timeline-step">
                            <div class="timeline-icon completed">✓</div>
                            <div>
                                <div style="font-weight: 700; font-size: 0.9rem; color: #0f172a;">2. Broadcasted to Public Sighting Radar</div>
                                <div style="font-size: 0.8rem; color: #64748b;">Available for citizen photo/video uploads</div>
                            </div>
                        </div>

                        <div class="timeline-step">
                            <div class="timeline-icon {'completed' if is_found else 'active'}">{'✓' if is_found else '⚙️'}</div>
                            <div>
                                <div style="font-weight: 700; font-size: 0.9rem; color: #0f172a;">3. AI Facial Recognition Scanning</div>
                                <div style="font-size: 0.8rem; color: #64748b;">{'Match confirmed with sighting report' if is_found else 'Active scanning across public uploads'}</div>
                            </div>
                        </div>

                        <div class="timeline-step">
                            <div class="timeline-icon {'completed' if is_found else ''}">{'✓' if is_found else '4'}</div>
                            <div>
                                <div style="font-weight: 700; font-size: 0.9rem; color: #0f172a;">4. Case Resolution & Complainant Notice</div>
                                <div style="font-size: 0.8rem; color: #64748b;">{'Resolved & complainant notified via email' if is_found else 'Pending AI match confirmation'}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Matched Sighting info if Found
            if case_obj.matched_with:
                matched_id = case_obj.matched_with.replace("{", "").replace("}", "").strip()
                matched_details = db_queries.get_public_case_detail(matched_id)
                if matched_details:
                    p = matched_details[0]
                    st.markdown(
                        f"""
                        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 1.2rem; margin-top: 1rem;">
                            <div style="font-weight: 700; font-size: 1rem; color: #166534; margin-bottom: 0.4rem;">
                                🎉 Verified Match Details:
                            </div>
                            <div style="font-size: 0.88rem; color: #15803d; line-height: 1.6;">
                                <div>📍 <strong>Location Spotted:</strong> {p[0]}</div>
                                <div>👤 <strong>Reported By:</strong> {p[1]} (Mobile: {p[2]})</div>
                                <div>🔍 <strong>Sighting Notes:</strong> {p[3]}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown("</div>", unsafe_allow_html=True)
