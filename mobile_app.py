import os
import uuid
import json
import tempfile

import streamlit as st

from pages.helper import db_queries
from pages.helper.data_models import PublicSubmissions
from pages.helper.utils import (
    image_obj_to_numpy,
    extract_face_mesh_landmarks,
    extract_unique_faces_from_video,
)
from pages.helper import ui_theme

st.set_page_config(
    page_title="Public Sighting Report • Missing Person AI",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Custom Law Enforcement Styling
ui_theme.inject_custom_theme()

# Page Header
ui_theme.render_header(
    title="Public Emergency Sighting Report",
    subtitle="Help locate missing individuals — Upload photographs or video recordings taken in public locations",
    badge="CITIZEN REPORTING PORTAL",
    icon="📢"
)

# Citizen Reassurance Notice
st.markdown(
    """
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 15px;">
        <div style="font-size: 2.2rem;">🤝</div>
        <div>
            <div style="font-weight: 700; color: #1e40af; font-size: 1rem;">Direct Dispatch to Law Enforcement Authorities</div>
            <div style="font-size: 0.88rem; color: #1e3a8a; margin-top: 2px;">
                Your submission is immediately indexed into station AI matching systems. Your contact details are kept strictly confidential.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

upload_mode = st.radio(
    "Select Submission Media Type",
    options=["📷 Photograph Upload", "🎥 Video Recording Upload"],
    horizontal=True,
)

image_col, form_col = st.columns([1, 1], gap="large")
save_flag = 0
extracted_faces = []
face_mesh = None
face_detected = False
unique_id = None
uploaded_file_path = None

# ── Image Upload ──────────────────────────────────────────────────────────────
if "Photograph" in upload_mode:
    with image_col:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 📷 Step 1: Upload Photo Sighting")
        st.caption("Upload a photograph showing the person's face clearly.")

        image_obj = st.file_uploader(
            "Choose Photo File", type=["jpg", "jpeg", "png"], key="user_submission_img"
        )
        if image_obj:
            unique_id = str(uuid.uuid4())

            with st.spinner("Processing facial landmark recognition..."):
                uploaded_file_path = "./resources/" + unique_id + ".jpg"
                with open(uploaded_file_path, "wb") as f:
                    f.write(image_obj.read())

                image_obj.seek(0)
                st.image(image_obj, use_container_width=True, caption="Uploaded Evidence")
                image_obj.seek(0)
                image_numpy = image_obj_to_numpy(image_obj)
                face_mesh = extract_face_mesh_landmarks(image_numpy)

                if face_mesh is None:
                    if uploaded_file_path and os.path.exists(uploaded_file_path):
                        os.remove(uploaded_file_path)
                    st.error("❌ **No face detected in this photo.** Please upload a clearer front-facing photo.")
                else:
                    face_detected = True
                    st.success("✅ **Face Landmark Coordinates Extracted (468 points).**")

        st.markdown("</div>", unsafe_allow_html=True)

    with form_col:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Step 2: Reporter & Location Details")

        if not image_obj or not face_detected:
            st.info("ℹ️ Upload a photograph with a detected face to activate the sighting report form.")
        else:
            with st.form(key="image_submission_form"):
                sub_name = st.text_input("Your Full Name *", placeholder="e.g. Ankit Kumar")
                mobile_number = st.text_input("Your Mobile Number * (10 digits)", placeholder="10-digit primary contact")
                email = st.text_input("Your Email (optional)", placeholder="email@domain.com")
                address = st.text_input("Location where person was spotted *", placeholder="e.g. Metro Station Gate 3, Connaught Place, Delhi")
                birth_marks = st.text_input("Distinguishing Features / Clothing", placeholder="e.g. Red jacket, blue backpack, scar on chin")

                st.markdown("<br>", unsafe_allow_html=True)
                submit_bt = st.form_submit_button("🚀 Submit Sighting Report")

                if submit_bt:
                    errors = []
                    if not sub_name.strip():
                        errors.append("Your Name is required.")
                    if not mobile_number.strip():
                        errors.append("Mobile Number is required.")
                    elif not mobile_number.strip().isdigit() or len(mobile_number.strip()) != 10:
                        errors.append("Mobile Number must be exactly 10 digits.")
                    if not address.strip():
                        errors.append("Location where person was spotted is required.")

                    if errors:
                        for err in errors:
                            st.error(f"❌ {err}")
                    else:
                        details = PublicSubmissions(
                            submitted_by=sub_name.strip(),
                            location=address.strip(),
                            email=email.strip() or None,
                            face_mesh=json.dumps(face_mesh),
                            id=unique_id,
                            mobile=mobile_number.strip(),
                            birth_marks=birth_marks.strip() or None,
                            status="NF",
                        )
                        db_queries.new_public_case(details)
                        save_flag = 1

            if save_flag == 1:
                st.balloons()
                st.success("🎉 **Report Received! Thank you for assisting law enforcement.**")
                st.info("Your report has been dispatched to station officers for AI landmark matching.")

        st.markdown("</div>", unsafe_allow_html=True)

# ── Video Upload ──────────────────────────────────────────────────────────────
else:
    with image_col:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 🎥 Step 1: Upload Video Sighting")
        st.caption("Upload a short video recording (MP4, MOV, AVI). The AI extracts unique individual faces from video frames.")

        video_obj = st.file_uploader(
            "Choose Video File", type=["mp4", "mov", "avi"], key="user_submission_video"
        )
        if video_obj:
            with st.spinner("🎥 Analyzing video frames and extracting unique faces..."):
                suffix = "." + video_obj.name.rsplit(".", 1)[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(video_obj.read())
                    tmp_path = tmp.name

                extracted_faces = extract_unique_faces_from_video(tmp_path)
                os.unlink(tmp_path)

                if not extracted_faces:
                    st.error("❌ **No faces detected in the video.** Ensure video has clear lighting and visible faces.")
                else:
                    st.success(f"✅ **Successfully extracted {len(extracted_faces)} unique face(s) from video.**")
                    st.caption("Extracted Face Frames:")
                    thumb_cols = st.columns(min(len(extracted_faces), 4))
                    for idx, (_, frame_rgb) in enumerate(extracted_faces):
                        thumb_cols[idx % 4].image(frame_rgb, use_container_width=True, caption=f"Face {idx+1}")

        st.markdown("</div>", unsafe_allow_html=True)

    with form_col:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Step 2: Reporter & Location Details")

        if not extracted_faces:
            st.info("ℹ️ Upload a video showing person's face to activate the sighting report form.")
        else:
            with st.form(key="video_submission_form"):
                sub_name = st.text_input("Your Full Name *", placeholder="e.g. Ankit Kumar")
                mobile_number = st.text_input("Your Mobile Number * (10 digits)", placeholder="10-digit primary contact")
                email = st.text_input("Your Email (optional)", placeholder="email@domain.com")
                address = st.text_input("Location where video was recorded *", placeholder="e.g. Bus Stand Sector 62, Noida")
                birth_marks = st.text_input("Distinguishing Features / Clothing", placeholder="e.g. Black jacket, white shoes")

                st.markdown("<br>", unsafe_allow_html=True)
                submit_bt = st.form_submit_button(f"🚀 Submit {len(extracted_faces)} Extracted Face Report(s)")

                if submit_bt:
                    errors = []
                    if not sub_name.strip():
                        errors.append("Your Name is required.")
                    if not mobile_number.strip():
                        errors.append("Mobile Number is required.")
                    elif not mobile_number.strip().isdigit() or len(mobile_number.strip()) != 10:
                        errors.append("Mobile Number must be exactly 10 digits.")
                    if not address.strip():
                        errors.append("Location is required.")

                    if errors:
                        for err in errors:
                            st.error(f"❌ {err}")
                    else:
                        count = 0
                        for landmarks, _ in extracted_faces:
                            sub_id = str(uuid.uuid4())
                            details = PublicSubmissions(
                                submitted_by=sub_name.strip(),
                                location=address.strip(),
                                email=email.strip() or None,
                                face_mesh=json.dumps(landmarks),
                                id=sub_id,
                                mobile=mobile_number.strip(),
                                birth_marks=birth_marks.strip() or None,
                                status="NF",
                            )
                            db_queries.new_public_case(details)
                            count += 1
                        save_flag = 1
                        st.balloons()
                        st.success(f"🎉 **Successfully received {count} face submission(s)! Thank you for assisting law enforcement.**")

        st.markdown("</div>", unsafe_allow_html=True)
