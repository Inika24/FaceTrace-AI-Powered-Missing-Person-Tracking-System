import os
import streamlit as st
import pandas as pd

from pages.helper import db_queries, emailer
from pages.helper.pdf_generator import generate_missing_person_pdf
from pages.helper import ui_theme

PAGE_SIZE = 8

st.set_page_config(
    page_title="All Cases • Missing Person AI",
    page_icon="📋",
    layout="wide"
)

ui_theme.inject_custom_theme()


def _reset_page(key: str):
    """Reset pagination when filters change."""
    st.session_state[key] = 0


# ── Case Cards Renderers ──────────────────────────────────────────────────────

def case_viewer(case, is_admin: bool = False):
    case = list(case)
    case_id = case.pop(0)  # index 0 → id

    matched_with_id = ""
    try:
        matched_with_id = case.pop(-1) or ""  # last item → matched_with
        matched_with_id = matched_with_id.replace("{", "").replace("}", "").strip()
    except Exception:
        matched_with_id = ""

    matched_with_details = None
    if matched_with_id:
        matched_with_details = db_queries.get_public_case_detail(matched_with_id)

    name = case[0] if len(case) > 0 else "Unknown"
    age = case[1] if len(case) > 1 else "N/A"
    raw_status = case[2] if len(case) > 2 else "NF"
    last_seen = case[3] if len(case) > 3 else "Unknown"

    status_pill = ui_theme.render_status_badge(raw_status)

    st.markdown(
        f"""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.8rem;">
                <div>
                    <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.25rem; font-weight: 700; color: #0f172a; margin: 0;">
                        👤 {name} <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">(Age: {age})</span>
                    </h3>
                    <div style="font-size: 0.85rem; color: #475569; margin-top: 2px;">
                        📍 <strong>Last Seen:</strong> {last_seen}
                    </div>
                </div>
                <div>{status_pill}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    image_col, info_col, matched_col = st.columns([1, 2, 2])

    case_detail_rows = db_queries.get_registered_case_detail(case_id)
    comp_phone, comp_email, comp_name, birthmarks = "N/A", "N/A", "N/A", "None"
    city_val = "N/A"

    if case_detail_rows and len(case_detail_rows[0]) > 0:
        row = case_detail_rows[0]
        comp_name = row[0] if len(row) > 0 else "N/A"
        comp_phone = row[1] if len(row) > 1 else "N/A"
        comp_email = row[2] if len(row) > 2 else "N/A"
        birthmarks = row[5] if len(row) > 5 else "None"

    with image_col:
        try:
            st.image(
                "./resources/" + str(case_id) + ".jpg",
                use_container_width=True,
            )
        except Exception:
            st.markdown(
                """
                <div style="background: #f1f5f9; border-radius: 10px; height: 120px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 0.85rem;">
                    No Image
                </div>
                """,
                unsafe_allow_html=True,
            )

    with info_col:
        st.markdown(
            f"""
            <div style="font-size: 0.88rem; color: #334155; line-height: 1.6;">
                <div><strong>📞 Complainant Phone:</strong> {comp_phone}</div>
                <div><strong>📧 Complainant Email:</strong> {comp_email}</div>
                <div><strong>🔍 Birthmarks:</strong> {birthmarks}</div>
                <div style="margin-top: 4px;"><strong>🔑 Tracking Case ID:</strong> <code style="color:#1d4ed8; font-weight:700;">{case_id}</code></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # PDF Poster Download Button
        pdf_details = {
            "id": case_id,
            "name": name,
            "age": age,
            "last_seen": last_seen,
            "city": city_val,
            "complainant_name": comp_name,
            "complainant_mobile": comp_phone,
            "birth_marks": birthmarks
        }
        try:
            pdf_path = generate_missing_person_pdf(pdf_details)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Official PDF Wanted Poster (with QR)",
                    data=pdf_file,
                    file_name=f"MISSING_ALERT_{case_id[:8]}.pdf",
                    mime="application/pdf",
                    key=f"pdf_btn_{case_id}"
                )
        except Exception as pdf_err:
            st.caption(f"PDF poster generation: {pdf_err}")

    with matched_col:
        if matched_with_details:
            st.markdown(
                f"""
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 0.8rem; font-size: 0.85rem; color: #166534;">
                    <div style="font-weight: 700; margin-bottom: 4px;">✅ Matched Citizen Sighting</div>
                    <div><strong>Location Seen:</strong> {matched_with_details[0][0]}</div>
                    <div><strong>Reported By:</strong> {matched_with_details[0][1]}</div>
                    <div><strong>Reporter Mobile:</strong> {matched_with_details[0][2]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px; padding: 0.8rem; font-size: 0.82rem; color: #64748b; text-align: center;">
                    🔍 No automated AI match confirmed yet.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Admin Actions Row
    if is_admin:
        st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
        act_col1, act_col2 = st.columns([1, 1])

        with act_col1:
            if raw_status == "F":
                if st.button("📧 Send Email Notification", key=f"email_{case_id}"):
                    if case_detail_rows:
                        sent = emailer.send_match_notification(case_id, case_detail_rows[0])
                        if sent:
                            complainant_email = case_detail_rows[0][2] if len(case_detail_rows[0]) > 2 else None
                            st.success(f"✅ Notification dispatched to {complainant_email or 'complainant'}.")
                        else:
                            st.warning("⚠️ SMTP email could not be sent. Check emailer configuration.")

        with act_col2:
            with st.expander("⚙️ Edit / Delete Case Record"):
                with st.form(key=f"edit_{case_id}"):
                    new_name = st.text_input("Name", value=name)
                    new_last_seen = st.text_input("Last Seen Location", value=last_seen)
                    save_btn = st.form_submit_button("💾 Save Changes")
                    if save_btn:
                        db_queries.update_registered_case(
                            case_id, {"name": new_name, "last_seen": new_last_seen}
                        )
                        st.success("Record updated successfully.")
                        st.rerun()

                st.markdown("---")
                confirm = st.checkbox("Confirm permanent deletion", key=f"del_confirm_{case_id}")
                if st.button("🗑️ Delete Record", key=f"del_{case_id}", type="primary"):
                    if confirm:
                        db_queries.delete_registered_case(case_id)
                        st.success("Case permanently deleted.")
                        st.rerun()
                    else:
                        st.warning("Please tick the confirmation checkbox first.")

    st.markdown("</div>", unsafe_allow_html=True)


def public_case_viewer(case: list) -> None:
    case = list(case)
    case_id = str(case.pop(0))

    raw_status = case[0] if len(case) > 0 else "NF"
    location = case[1] if len(case) > 1 else "Unknown"
    mobile = case[2] if len(case) > 2 else "N/A"
    birthmarks = case[3] if len(case) > 3 else "N/A"
    submitted_on = str(case[4])[:16] if len(case) > 4 else "N/A"
    submitted_by = case[5] if len(case) > 5 else "Anonymous Citizen"

    status_pill = ui_theme.render_status_badge(raw_status)

    st.markdown(
        f"""
        <div class="custom-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
                <div>
                    <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.15rem; font-weight: 700; color: #0f172a; margin: 0;">
                        📢 Public Citizen Sighting Report
                    </h3>
                    <div style="font-size: 0.85rem; color: #64748b;">Submitted by <strong>{submitted_by}</strong> on {submitted_on}</div>
                </div>
                <div>{status_pill}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    image_col, info_col = st.columns([1, 4])

    with image_col:
        try:
            st.image("./resources/" + case_id + ".jpg", use_container_width=True)
        except Exception:
            st.caption("No Image")

    with info_col:
        st.markdown(
            f"""
            <div style="font-size: 0.88rem; color: #334155; line-height: 1.6;">
                <div><strong>📍 Location Sighting:</strong> {location}</div>
                <div><strong>📞 Reporter Contact:</strong> {mobile}</div>
                <div><strong>🔍 Distinguishing Features:</strong> {birthmarks}</div>
                <div><strong>🔑 Submission Tracking ID:</strong> <code>{case_id}</code></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ── Pagination Helper ─────────────────────────────────────────────────────────

def paginate(items: list, page_key: str):
    """Return the current page slice and render Prev / Next controls."""
    total = len(items)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = st.session_state.get(page_key, 0)
    page = max(0, min(page, total_pages - 1))
    st.session_state[page_key] = page

    paginated = items[page * PAGE_SIZE : (page + 1) * PAGE_SIZE]

    def render_controls():
        c_prev, c_info, c_next = st.columns([1, 3, 1])
        if c_prev.button("◀ Previous Page", disabled=page == 0, key=f"{page_key}_prev"):
            st.session_state[page_key] = page - 1
            st.rerun()
        c_info.markdown(
            f"<div style='text-align:center; padding-top:8px; font-weight:600; color:#475569;'>Page {page + 1} of {total_pages} &nbsp;·&nbsp; {total} record(s)</div>",
            unsafe_allow_html=True,
        )
        if c_next.button("Next Page ▶", disabled=page >= total_pages - 1, key=f"{page_key}_next"):
            st.session_state[page_key] = page + 1
            st.rerun()

    return paginated, render_controls


# ── Main Page Logic ───────────────────────────────────────────────────────────

if "login_status" not in st.session_state or not st.session_state["login_status"]:
    ui_theme.render_header(
        title="View & Manage Registered Cases",
        subtitle="Filter missing person complaints, inspect citizen sighting reports, and manage official case records",
        badge="CASE REPOSITORY DATABASE",
        icon="📋"
    )
    ui_theme.render_login_prompt("Viewing All Registered Cases")
    st.stop()

user = st.session_state.user
is_admin = st.session_state.get("role", "").lower() == "admin"

ui_theme.render_header(
    title="View & Manage Registered Cases",
    subtitle="Filter missing person complaints, inspect citizen sighting reports, and manage official case records",
    badge="CASE REPOSITORY DATABASE",
    icon="📋"
)

# ── Filter Bar Card ───────────────────────────────────────────────────────────
f_col1, f_col2, f_col3 = st.columns([2, 3, 2])

status = f_col1.selectbox(
    "Filter by Status / Category",
    options=["All", "Not Found", "Found", "Public Cases"],
    on_change=_reset_page,
    args=("page_reg",),
)

search_name = f_col2.text_input(
    "🔍 Search by Name or ID",
    placeholder="Type a name to instantly filter...",
    on_change=_reset_page,
    args=("page_reg",),
)

date_filter = f_col3.date_input("Filter by Registration Date", value=None)

# ── Public Cases View ─────────────────────────────────────────────────────────
if status == "Public Cases":
    cases_data = list(db_queries.fetch_public_cases(False, status))

    if search_name:
        cases_data = [c for c in cases_data if search_name.lower() in str(c).lower()]

    if date_filter:
        cases_data = [c for c in cases_data if c[5] and str(c[5])[:10] >= str(date_filter)]

    if cases_data:
        df = pd.DataFrame(
            cases_data,
            columns=[
                "ID",
                "Status",
                "Location",
                "Mobile",
                "Birth Marks",
                "Submitted On",
                "Submitted By",
            ],
        )
        df["Status"] = df["Status"].map({"F": "Found", "NF": "Not Found"}).fillna(df["Status"])
        st.download_button(
            "📥 Export Public Cases CSV",
            data=df.to_csv(index=False),
            file_name="public_sightings_export.csv",
            mime="text/csv",
        )

    if not cases_data:
        st.info("ℹ️ No public citizen sighting records match your search criteria.")
    else:
        paginated, render_controls = paginate(cases_data, "page_pub")
        for case in paginated:
            public_case_viewer(case)
        render_controls()

# ── Registered Cases View ─────────────────────────────────────────────────────
else:
    cases_data = list(db_queries.fetch_registered_cases(user, status))

    if search_name:
        cases_data = [c for c in cases_data if search_name.lower() in str(c[1]).lower()]

    if date_filter:
        from sqlmodel import Session, select
        from pages.helper.db_queries import engine
        from pages.helper.data_models import RegisteredCases
        import datetime

        date_dt = datetime.datetime.combine(date_filter, datetime.time.min)
        with Session(engine) as session:
            q = (
                select(
                    RegisteredCases.id,
                    RegisteredCases.name,
                    RegisteredCases.age,
                    RegisteredCases.status,
                    RegisteredCases.last_seen,
                    RegisteredCases.matched_with,
                )
                .where(RegisteredCases.submitted_by == user)
                .where(RegisteredCases.submitted_on >= date_dt)
            )
            if status != "All":
                status_filter = "F" if status == "Found" else "NF"
                q = q.where(RegisteredCases.status == status_filter)
            cases_data = list(session.exec(q).all())

        if search_name:
            cases_data = [c for c in cases_data if search_name.lower() in str(c[1]).lower()]

    if cases_data:
        df = pd.DataFrame(
            cases_data,
            columns=["ID", "Name", "Age", "Status", "Last Seen", "Matched With"],
        )
        df["Status"] = df["Status"].map({"F": "Found", "NF": "Not Found"}).fillna(df["Status"])
        st.download_button(
            "📥 Export Registered Cases CSV",
            data=df.to_csv(index=False),
            file_name="registered_cases_export.csv",
            mime="text/csv",
        )

    if not cases_data:
        st.info("ℹ️ No registered cases found matching your filters.")
    else:
        paginated, render_controls = paginate(cases_data, "page_reg")
        for case in paginated:
            case_viewer(case, is_admin=is_admin)
        render_controls()
