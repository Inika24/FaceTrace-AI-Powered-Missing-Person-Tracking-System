import streamlit as st
from pages.helper import ui_theme

st.set_page_config(
    page_title="Help & Documentation • Missing Person AI",
    page_icon="❓",
    layout="wide"
)

ui_theme.inject_custom_theme()

ui_theme.render_header(
    title="Help & System Documentation Center",
    subtitle="Comprehensive user manuals, facial recognition technology specs, photo upload guidelines, and station support",
    badge="SYSTEM MANUAL v3.0",
    icon="❓"
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Officer User Guide",
    "🤖 AI Facial Recognition Specs",
    "📸 Photo & Video Standards",
    "❓ Frequently Asked Questions",
    "📞 Emergency & Station Support"
])

# ── Tab 1: Officer User Guide ────────────────────────────────────────────────
with tab1:
    st.markdown(
        """
        <div class="custom-card">
            <h3 style="color: #0f172a; margin-top: 0;">👮 Station Officer Workflow Guide</h3>
            <p style="color: #475569; font-size: 0.95rem;">
                Follow this step-by-step procedure when handling missing person complaints and citizen sightings:
            </p>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.2rem; height: 100%;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">1️⃣</div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #1e3a8a;">Register New Case</div>
                <p style="font-size: 0.85rem; color: #64748b; margin-top: 0.4rem;">
                    Upload a high-resolution front photograph under <strong>Register New Case</strong>. 
                    The system extracts 468 landmark points and generates a shareable <strong>Case Tracking Code</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.2rem; height: 100%;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">2️⃣</div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #1e3a8a;">Track Case Status</div>
                <p style="font-size: 0.85rem; color: #64748b; margin-top: 0.4rem;">
                    Share the Case ID with family members or officers. Anyone can paste the Case ID, Aadhaar number, or Name in <strong>Track Case</strong> to view live updates.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.2rem; height: 100%;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">3️⃣</div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #1e3a8a;">Public Sighting Reports</div>
                <p style="font-size: 0.85rem; color: #64748b; margin-top: 0.4rem;">
                    Citizens upload photo/video sightings via <strong>Report a Sighting</strong> which automatically index into the AI match queue.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
            <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.2rem; height: 100%;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">4️⃣</div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #1e3a8a;">AI Scan & Notify</div>
                <p style="font-size: 0.85rem; color: #64748b; margin-top: 0.4rem;">
                    Admins trigger KNN matching under <strong>Match Cases</strong>. When a match occurs, case status becomes <em>Found</em> and automated email notifications dispatch.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ── Tab 2: AI Technology Specs ───────────────────────────────────────────────
with tab2:
    st.markdown(
        """
        <div class="custom-card">
            <h3 style="color: #0f172a; margin-top: 0;">🔬 AI Facial Landmark Pipeline Architecture</h3>
            <p style="color: #475569; font-size: 0.95rem;">
                The platform utilizes a multi-tiered Computer Vision and Machine Learning pipeline optimized for high precision and fast spatial retrieval:
            </p>
            
            <div style="background: #f1f5f9; border-radius: 10px; padding: 1.2rem; margin: 1rem 0; font-family: monospace; font-size: 0.88rem; color: #1e293b;">
                <strong>PIPELINE FLOW:</strong><br>
                [Image / Video Upload] ➔ [MediaPipe Face Mesh (468 3D Points)] ➔ [L2 Normalization & Feature Embedding] ➔ [K-Nearest Neighbors (KNN) Distance Metric (k=1)] ➔ [Automated Match & Complainant Notification]
            </div>

            <h4 style="color: #1d4ed8; margin-top: 1.2rem;">Key Technical Components:</h4>
            <ul style="color: #334155; font-size: 0.92rem; line-height: 1.7;">
                <li><strong>MediaPipe Face Mesh:</strong> Detects 468 3D facial landmarks per face in real-time, providing high robustness against minor lighting variations and pose shifts.</li>
                <li><strong>KNN Classification:</strong> K-Nearest Neighbors vector space algorithm maps 3D landmark geometric distances to evaluate similarity confidence scores (0–100%).</li>
                <li><strong>Multi-Face Detection:</strong> Supports extracting up to 5 individual faces per photograph or extracting unique facial frames from uploaded citizen videos.</li>
                <li><strong>SQLModel & PostgreSQL Database:</strong> Case records and serialized 468 3D facial landmark vectors are stored in PostgreSQL / SQLModel relational database architecture with indexing on station user boundaries.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Tab 3: Photo & Video Standards ───────────────────────────────────────────
with tab3:
    st.markdown(
        """
        <div class="custom-card">
            <h3 style="color: #0f172a; margin-top: 0;">📸 Photograph & Video Submission Guidelines</h3>
            <p style="color: #475569; font-size: 0.95rem;">
                To maximize facial recognition match confidence, ensure uploaded images meet the following criteria:
            </p>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin-top: 1rem;">
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 1.2rem;">
                    <h4 style="color: #166534; margin-top: 0;">✅ DOs (Optimal Quality)</h4>
                    <ul style="color: #15803d; font-size: 0.88rem; line-height: 1.6; padding-left: 1.2rem;">
                        <li>Use clear, front-facing eye-level photographs.</li>
                        <li>Ensure even facial lighting with minimal deep shadows.</li>
                        <li>Keep neutral or natural facial expressions.</li>
                        <li>Ensure minimum resolution of 400x400 pixels.</li>
                        <li>For video uploads, ensure person is visible for at least 2–3 seconds.</li>
                    </ul>
                </div>

                <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 1.2rem;">
                    <h4 style="color: #991b1b; margin-top: 0;">❌ DON'Ts (Avoid)</h4>
                    <ul style="color: #b91c1c; font-size: 0.88rem; line-height: 1.6; padding-left: 1.2rem;">
                        <li>Avoid extreme side profile angles (>45° pitch/yaw).</li>
                        <li>Do not upload heavily pixelated, blurry, or low-light photos.</li>
                        <li>Avoid face coverings, heavy sunglasses, or masks obscuring eyes/nose.</li>
                        <li>Avoid photos with heavy artistic filters or distortion.</li>
                    </ul>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Tab 4: FAQ ───────────────────────────────────────────────────────────────
with tab4:
    st.markdown("### ❓ Frequently Asked Questions")

    with st.expander("Q1: How can I or family members track a registered case?"):
        st.write(
            "Every registered case generates a unique **Case Tracking ID**. Anyone (officers, family members, or citizens) "
            "can go to the **Track Case** tab and paste the Case ID, Aadhaar number, or Name to view live status updates and timeline."
        )

    with st.expander("Q2: What happens when a match is found during an AI scan?"):
        st.write(
            "When the KNN matching engine identifies a landmark similarity distance below 3.0, the registered case status "
            "is automatically updated from 'Not Found' to 'Found'. The matched public sighting details (location, reporter phone, birthmarks) "
            "are linked to the case, and an automated email notification is sent to the complainant's email address."
        )

    with st.expander("Q3: Who can trigger the AI Matching Scan?"):
        st.write(
            "For security and verification integrity, only accounts assigned the **ADMIN** role can trigger the matching pipeline under the 'Match Cases' tab."
        )

    with st.expander("Q4: Can citizens report sightings without logging into the officer portal?"):
        st.write(
            "Yes! The public citizen portal is accessible via `mobile_app.py` or the **Report a Sighting** menu page."
        )

# ── Tab 5: Emergency Support ─────────────────────────────────────────────────
with tab5:
    st.markdown(
        """
        <div class="custom-card">
            <h3 style="color: #0f172a; margin-top: 0;">📞 Station Support & Emergency Contacts</h3>
            <p style="color: #475569; font-size: 0.95rem;">
                For technical issues, database resets, or emergency assistance, contact system administration:
            </p>

            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.2rem; font-size: 0.92rem; color: #334155; line-height: 1.8;">
                <div>🚨 <strong>Emergency Police Helpline:</strong> 112 / 100</div>
                <div>🏢 <strong>Station Officer In-Charge:</strong> Inika B (inikab@gmail.com)</div>
                <div>📍 <strong>Jurisdiction Area:</strong> Avinashi, Tiruppur</div>
                <div>⚙️ <strong>System IT Support Desk:</strong> support-ai@police.gov.in</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
