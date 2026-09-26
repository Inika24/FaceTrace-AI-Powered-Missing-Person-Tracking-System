import os
import uuid
import json
import tempfile
import streamlit as st

from sqlmodel import Session, select
from pages.helper.db_queries import engine
from pages.helper.data_models import RegisteredCases, PublicSubmissions
from pages.helper import db_queries
from pages.helper.utils import (
    image_obj_to_numpy,
    extract_face_mesh_landmarks,
    extract_unique_faces_from_video,
)
from pages.helper import ui_theme

st.set_page_config(
    page_title="Report a Sighting • Missing Person AI",
    page_icon="👁️",
    layout="wide"
)

ui_theme.inject_custom_theme()

ui_theme.render_header(
    title="Report a Missing Person Sighting",
    subtitle="I saw this person — Submit photo/video sighting evidence linked by Aadhaar, Phone, Name, or Case ID",
    badge="CITIZEN & OFFICER SIGHTING MODULE",
    icon="👁️"
)

# Step 1: Missing Person Lookup
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.markdown("### 🔍 Step 1: Find the Missing Person Record")
st.caption("Search by Aadhaar Card Number, Complainant Phone Number, Person Name, or Case ID.")

search_query = st.text_input(
    "Search Missing Person Record",
    placeholder="Type Aadhaar (12 digits), Mobile (10 digits), Person Name, or Case ID...",
    key="sighting_search_input"
)

matched_cases = []
if search_query.strip():
    q = search_query.strip().lower()
    with Session(engine) as session:
        all_cases = session.exec(select(RegisteredCases)).all()
        for c in all_cases:
            if (
                q == c.id.lower()
                or q in c.name.lower()
                or (c.adhaar_card and q in c.adhaar_card.lower())
                or (c.complainant_mobile and q in c.complainant_mobile.lower())
                or (c.complainant_name and q in c.complainant_name.lower())
            ):
                matched_cases.append(c)

selected_case = None
if matched_cases:
    st.success(f"✅ Found {len(matched_cases)} matching record(s). Select the person you spotted:")
    case_options = {f"{c.name} (Age: {c.age}, Last Seen: {c.last_seen}, City: {c.city or 'N/A'}) — ID: {c.id[:8]}...": c for c in matched_cases}
    chosen_label = st.selectbox("Select Target Person", list(case_options.keys()))
    selected_case = case_options[chosen_label]

    st.markdown(
        f"""
        <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 12px; padding: 1rem; margin-top: 0.8rem; display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 2rem;">👤</div>
            <div>
                <div style="font-weight: 700; color: #0369a1; font-size: 1.05rem;">Target Case Selected: {selected_case.name}</div>
                <div style="font-size: 0.85rem; color: #0284c7;">
                    Aadhaar: {selected_case.adhaar_card or 'N/A'} &nbsp;·&nbsp; 
                    Complainant: {selected_case.complainant_name} ({selected_case.complainant_mobile}) &nbsp;·&nbsp;
                    Case ID: <code>{selected_case.id}</code>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif search_query.strip():
    st.warning("⚠️ No exact record found. You can still submit a general sighting below!")

st.markdown("</div>", unsafe_allow_html=True)

# Step 2: Upload Evidence & Location Details
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.markdown("### 📸 Step 2: Sighting Location & Photo/Video Evidence")

upload_mode = st.radio(
    "Media Type",
    options=["📷 Photograph", "🎥 Video Recording"],
    horizontal=True,
    key="sighting_media_mode"
)

col_left, col_right = st.columns([1, 1], gap="large")
face_mesh = None
extracted_faces = []
face_detected = False
save_flag = 0

with col_left:
    if "Photograph" in upload_mode:
        img_file = st.file_uploader("Upload Sighting Photo", type=["jpg", "jpeg", "png"], key="sighting_img")
        if img_file:
            unique_id = str(uuid.uuid4())
            file_path = "./resources/" + unique_id + ".jpg"
            with open(file_path, "wb") as f:
                f.write(img_file.read())
            img_file.seek(0)
            st.image(img_file, use_container_width=True, caption="Sighting Photo Evidence")
            img_file.seek(0)

            with st.spinner("Extracting 468 AI facial landmarks..."):
                img_np = image_obj_to_numpy(img_file)
                face_mesh = extract_face_mesh_landmarks(img_np)

            if face_mesh is None:
                if os.path.exists(file_path):
                    os.remove(file_path)
                st.error("❌ No face detected in photo. Please ensure face is clearly visible.")
            else:
                face_detected = True
                st.success("✅ 468 Facial Landmark Points Extracted!")
    else:
        vid_file = st.file_uploader("Upload Sighting Video", type=["mp4", "mov", "avi"], key="sighting_video")
        if vid_file:
            with st.spinner("Analyzing video frames for faces..."):
                suffix = "." + vid_file.name.rsplit(".", 1)[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(vid_file.read())
                    tmp_path = tmp.name

                extracted_faces = extract_unique_faces_from_video(tmp_path)
                os.unlink(tmp_path)

                if not extracted_faces:
                    st.error("❌ No faces detected in video frames.")
                else:
                    face_detected = True
                    st.success(f"✅ Found {len(extracted_faces)} unique face(s) in video.")
                    thumb_cols = st.columns(min(len(extracted_faces), 4))
                    for idx, (_, frame_rgb) in enumerate(extracted_faces):
                        thumb_cols[idx % 4].image(frame_rgb, use_container_width=True, caption=f"Face {idx+1}")

with col_right:
    with st.form(key="sighting_form"):
        st.markdown("#### 📍 Location & Reporter Info")
        location = st.text_input("Exact Location / Landmark Spotted *", placeholder="e.g. Bus Stand, Avinashi, Tiruppur")
        sighting_time = st.text_input("Date & Time of Sighting", placeholder="e.g. 26th Sept 2026 at 5:30 PM")
        notes = st.text_area("Observations / Distinguishing Notes", placeholder="e.g. Wearing blue shirt, carried red bag")

        st.markdown("#### 👤 Your Contact Info")
        sub_name = st.text_input("Your Full Name *", placeholder="e.g. Inika B")
        mobile = st.text_input("Your Mobile Number * (10 digits)", placeholder="10-digit number")
        email = st.text_input("Your Email (optional)", placeholder="inikab@gmail.com")

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("🚀 Submit Sighting Report")

        if submit_btn:
            errors = []
            if not location.strip():
                errors.append("Location where person was spotted is required.")
            if not sub_name.strip():
                errors.append("Your Name is required.")
            if not mobile.strip() or not mobile.strip().isdigit() or len(mobile.strip()) != 10:
                errors.append("Valid 10-digit Mobile Number is required.")
            if not face_detected:
                errors.append("Please upload a photo or video with a detectable face.")

            if errors:
                for err in errors:
                    st.error(f"❌ {err}")
            else:
                if "Photograph" in upload_mode and face_mesh:
                    sub_id = str(uuid.uuid4())
                    details = PublicSubmissions(
                        submitted_by=sub_name.strip(),
                        location=f"{location.strip()} (Seen at: {sighting_time.strip()})",
                        email=email.strip() or None,
                        face_mesh=json.dumps(face_mesh),
                        id=sub_id,
                        mobile=mobile.strip(),
                        birth_marks=f"{notes.strip()}" + (f" | Linked to Case ID: {selected_case.id}" if selected_case else ""),
                        status="NF",
                    )
                    db_queries.new_public_case(details)
                    save_flag = 1
                elif extracted_faces:
                    for landmarks, _ in extracted_faces:
                        sub_id = str(uuid.uuid4())
                        details = PublicSubmissions(
                            submitted_by=sub_name.strip(),
                            location=f"{location.strip()} (Seen at: {sighting_time.strip()})",
                            email=email.strip() or None,
                            face_mesh=json.dumps(landmarks),
                            id=sub_id,
                            mobile=mobile.strip(),
                            birth_marks=f"{notes.strip()}" + (f" | Linked to Case ID: {selected_case.id}" if selected_case else ""),
                            status="NF",
                        )
                        db_queries.new_public_case(details)
                    save_flag = 1

if save_flag == 1:
    st.balloons()
    st.success("🎉 **Sighting Report Successfully Dispatched to Station Officers & AI Match Engine!**")
    if selected_case:
        st.info(f"💡 Report linked to Case ID **{selected_case.id}** for {selected_case.name}. Track live updates under **Track Case**.")

st.markdown("</div>", unsafe_allow_html=True)
