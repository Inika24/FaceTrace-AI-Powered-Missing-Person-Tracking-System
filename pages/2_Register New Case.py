import os
import uuid
import json

import streamlit as st

from pages.helper.data_models import RegisteredCases
from pages.helper import db_queries
from pages.helper.utils import image_obj_to_numpy, detect_all_faces, draw_face_boxes
from pages.helper import ui_theme

st.set_page_config(
    page_title="Register New Case • Missing Person AI",
    page_icon="📝",
    layout="wide"
)

ui_theme.inject_custom_theme()

if "login_status" not in st.session_state or not st.session_state["login_status"]:
    ui_theme.render_header(
        title="Register New Missing Person Case",
        subtitle="Upload photo and person details to index into AI matching network",
        badge="OFFICIAL REGISTRATION",
        icon="📝"
    )
    ui_theme.render_login_prompt("Registering a Case")
    st.stop()

user = st.session_state.user

ui_theme.render_header(
    title="Register New Missing Person Case",
    subtitle="Upload front-facing facial photo to extract 468 AI landmark points and generate shareable tracking code",
    badge="OFFICIAL REGISTRATION FORM",
    icon="📝"
)

# Step Progress Bar Visual
st.markdown(
    """
    <div style="background: #ffffff; padding: 1rem 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 1.5rem; display: flex; justify-content: space-around; align-items: center; text-align: center;">
        <div style="flex: 1;">
            <span style="background: #1d4ed8; color: white; border-radius: 50%; padding: 4px 10px; font-weight: 700; font-size: 0.85rem;">1</span>
            <div style="font-size: 0.85rem; font-weight: 700; color: #0f172a; margin-top: 4px;">Upload & Face Mesh</div>
        </div>
        <div style="height: 2px; background: #cbd5e1; flex: 0.5;"></div>
        <div style="flex: 1;">
            <span style="background: #1d4ed8; color: white; border-radius: 50%; padding: 4px 10px; font-weight: 700; font-size: 0.85rem;">2</span>
            <div style="font-size: 0.85rem; font-weight: 700; color: #0f172a; margin-top: 4px;">Person Profile</div>
        </div>
        <div style="height: 2px; background: #cbd5e1; flex: 0.5;"></div>
        <div style="flex: 1;">
            <span style="background: #1d4ed8; color: white; border-radius: 50%; padding: 4px 10px; font-weight: 700; font-size: 0.85rem;">3</span>
            <div style="font-size: 0.85rem; font-weight: 700; color: #0f172a; margin-top: 4px;">Tracking ID & Share</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

image_col, form_col = st.columns([1, 1], gap="large")
save_flag = 0
registered_case_id = None

with image_col:
    st.markdown("### 📸 Step 1: Upload Photograph")
    st.caption("Upload a front-facing image of the missing person (JPG, JPEG, PNG).")

    image_obj = st.file_uploader(
        "Choose Photograph", type=["jpg", "jpeg", "png"], key="new_case_photo"
    )

    if image_obj:
        file_key = f"{image_obj.name}_{image_obj.size}"

        if st.session_state.get("nc_file_key") != file_key:
            unique_id = str(uuid.uuid4())
            uploaded_file_path = "./resources/" + unique_id + ".jpg"

            with open(uploaded_file_path, "wb") as f:
                f.write(image_obj.read())
            image_obj.seek(0)

            with st.spinner("🔍 Running MediaPipe AI 3D Facial Landmark Extraction..."):
                image_numpy = image_obj_to_numpy(image_obj)
                faces = detect_all_faces(image_numpy, max_faces=5)

            if not faces:
                if os.path.exists(uploaded_file_path):
                    os.remove(uploaded_file_path)
                st.session_state["nc_file_key"] = file_key
                st.session_state["nc_faces"] = []
                st.session_state["nc_image_numpy"] = None
                st.session_state["nc_unique_id"] = None
                st.session_state["nc_uploaded_path"] = None
            else:
                st.session_state["nc_file_key"] = file_key
                st.session_state["nc_faces"] = faces
                st.session_state["nc_image_numpy"] = image_numpy
                st.session_state["nc_unique_id"] = unique_id
                st.session_state["nc_uploaded_path"] = uploaded_file_path

        faces = st.session_state.get("nc_faces", [])
        image_numpy = st.session_state.get("nc_image_numpy")
        unique_id = st.session_state.get("nc_unique_id")

        if not faces:
            st.error(
                "❌ **No face detected in this image.**\n\n"
                "**Tips for best results:**\n"
                "• Ensure adequate lighting with full front-facing camera angle\n"
                "• Avoid extreme side profiles, heavy motion blur, or obstructions"
            )
            selected_face_idx = None
        elif len(faces) == 1:
            annotated = draw_face_boxes(image_numpy, faces, selected_idx=0)
            st.image(annotated, use_container_width=True, caption="Verified Face mesh alignment (1 face detected)")
            st.success("✅ **1 Face Successfully Indexed** (468 Landmark Coordinates Extracted)")
            selected_face_idx = 0
        else:
            st.warning(f"⚠️ **Multiple ({len(faces)}) faces detected.** Please select the person to register:")
            options = [f"Face {i + 1}" for i in range(len(faces))]
            choice = st.radio("Select Target Face", options, horizontal=True, key="nc_face_choice")
            selected_face_idx = options.index(choice)
            annotated = draw_face_boxes(image_numpy, faces, selected_idx=selected_face_idx)
            st.image(annotated, use_container_width=True, caption=f"Selected: Face {selected_face_idx + 1}")
            st.info(f"Targeting **Face {selected_face_idx + 1}** for database indexing.")
    else:
        for k in ["nc_file_key", "nc_faces", "nc_image_numpy", "nc_unique_id", "nc_uploaded_path"]:
            st.session_state.pop(k, None)
        selected_face_idx = None
        unique_id = None
        faces = []

        st.info("ℹ️ Upload a photograph to unlock the registration form.")

# ── Form Column ──────────────────────────────────────────────────────────────
face_ready = image_obj and faces and selected_face_idx is not None

with form_col:
    st.markdown("### 📋 Step 2 & 3: Official Complaint & Tracking Code")

    if not face_ready:
        st.markdown(
            """
            <div style="background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 3rem 1.5rem; text-align: center; color: #64748b;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔒</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #334155;">Form Locked</div>
                <div>Please upload a valid face photograph on the left to activate registration fields.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        with st.form(key="new_case_form"):
            st.markdown("#### 👤 Missing Person Details")
            c1, c2 = st.columns(2)
            name = c1.text_input("Full Name *", placeholder="e.g. Ramesh Kumar")
            father_name = c2.text_input("Father / Guardian Name", placeholder="e.g. Balan K")

            c3, c4 = st.columns(2)
            age = c3.number_input("Age", min_value=1, max_value=120, value=22, step=1)
            mobile_number = c4.text_input("Mobile Number (10 digits)", placeholder="10-digit number")

            adhaar_card = st.text_input("Aadhaar Card Number (12 digits)", placeholder="12-digit Aadhaar ID")
            
            c5, c6 = st.columns(2)
            last_seen = c5.text_input("Last Seen Location *", placeholder="e.g. Bus Stand, Avinashi")
            city = c6.text_input("City *", placeholder="e.g. Tiruppur")

            address = st.text_input("Permanent Address", placeholder="Avinashi, Tiruppur")
            birthmarks = st.text_input("Birthmarks / Distinguishing Features", placeholder="e.g. Scar on left cheek, mole on chin")
            description = st.text_area("Additional Description / Clothing Details", placeholder="Clothing worn when last seen, medical conditions, etc.")

            st.markdown("---")
            st.markdown("#### 📞 Complainant / Relative Details")
            comp_name = st.text_input("Complainant Name *", value="Inika B")
            
            c7, c8 = st.columns(2)
            comp_phone = c7.text_input("Complainant Phone Number *", placeholder="10-digit primary phone")
            comp_email = c8.text_input("Complainant Email (for automated notifications)", value="inikab@gmail.com")

            st.markdown("<br>", unsafe_allow_html=True)
            submit_bt = st.form_submit_button("💾 Register Case & Generate Tracking Code")

            if submit_bt:
                errors = []
                if not name.strip():
                    errors.append("Name of missing person is required.")
                if not last_seen.strip():
                    errors.append("Last Seen location is required.")
                if not city.strip():
                    errors.append("City is required.")
                if not comp_name.strip():
                    errors.append("Complainant Name is required.")
                if not comp_phone.strip():
                    errors.append("Complainant Phone is required.")
                elif not comp_phone.strip().isdigit() or len(comp_phone.strip()) != 10:
                    errors.append("Complainant Phone must be exactly 10 numeric digits.")
                if mobile_number.strip() and (not mobile_number.strip().isdigit() or len(mobile_number.strip()) != 10):
                    errors.append("Missing person mobile number must be exactly 10 digits.")
                if adhaar_card.strip() and (not adhaar_card.strip().isdigit() or len(adhaar_card.strip()) != 12):
                    errors.append("Aadhaar Card number must be exactly 12 numeric digits.")

                if errors:
                    for err in errors:
                        st.error(f"❌ {err}")
                else:
                    selected_landmarks = faces[selected_face_idx]["landmarks"]
                    new_case_details = RegisteredCases(
                        id=unique_id,
                        submitted_by=user,
                        name=name.strip(),
                        father_name=father_name.strip(),
                        age=str(age),
                        complainant_mobile=comp_phone.strip(),
                        complainant_name=comp_name.strip(),
                        complainant_email=comp_email.strip() or None,
                        face_mesh=json.dumps(selected_landmarks),
                        adhaar_card=adhaar_card.strip(),
                        birth_marks=birthmarks.strip(),
                        address=address.strip(),
                        city=city.strip() or None,
                        last_seen=last_seen.strip(),
                        description=description.strip() or None,
                        status="NF",
                        matched_with="",
                    )
                    db_queries.register_new_case(new_case_details)
                    save_flag = 1
                    registered_case_id = unique_id

        if save_flag:
            st.balloons()
            st.success("🎉 **Case Successfully Registered and Indexed into Database.**")
            st.markdown(
                f"""
                <div class="tracking-box">
                    <div style="font-weight: 700; color: #0369a1; font-size: 0.9rem;">SHAREABLE CASE TRACKING CODE:</div>
                    <div class="tracking-code">{registered_case_id}</div>
                    <div style="font-size: 0.82rem; color: #0284c7; margin-top: 0.5rem;">
                        Anyone with this Case ID, Aadhaar number, or person name can track live AI status under the <strong>Track Case</strong> tab.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
