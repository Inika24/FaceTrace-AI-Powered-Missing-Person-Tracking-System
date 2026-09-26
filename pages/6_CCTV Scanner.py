import os
import tempfile
import streamlit as st
import pandas as pd
from PIL import Image

from pages.helper import db_queries
from pages.helper.cctv_engine import scan_video_stream
from pages.helper import ui_theme

st.set_page_config(
    page_title="CCTV Video Scanner • Missing Person AI",
    page_icon="📹",
    layout="wide"
)

ui_theme.inject_custom_theme()

if "login_status" not in st.session_state or not st.session_state["login_status"]:
    ui_theme.render_header(
        title="CCTV & Video Crowd Surveillance Console",
        subtitle="Real-time multi-person facial recognition scanning across surveillance footage",
        badge="SURVEILLANCE MODULE",
        icon="📹"
    )
    ui_theme.render_login_prompt("CCTV Video Scanner Console")
    st.stop()

user = st.session_state.user

ui_theme.render_header(
    title="Real-Time CCTV & Crowd Surveillance Console",
    subtitle="Automated frame-by-frame multi-person face scanning, bounding box detection, timestamp logging, & instant match alerts",
    badge="AUTOMATED SURVEILLANCE ENGINE",
    icon="📹"
)

st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.markdown("### 📹 Step 1: Input CCTV Footage / Video Feed")

video_source = st.file_uploader(
    "Upload CCTV Video File (MP4, MOV, AVI)",
    type=["mp4", "mov", "avi"],
    key="cctv_file_up"
)

c1, c2, c3 = st.columns(3)
frame_skip = c1.slider("Frame Sampling Frequency", min_value=1, max_value=30, value=5, help="Scan every Nth frame")
dist_thresh = c2.slider("Match Sensitivity Distance", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
run_btn = c3.button("⚡ Start CCTV Surveillance Scan", type="primary")

st.markdown("</div>", unsafe_allow_html=True)

if run_btn:
    if not video_source:
        st.warning("⚠️ Please upload a CCTV video file to execute surveillance scan.")
    else:
        suffix = "." + video_source.name.rsplit(".", 1)[-1]
        video_bytes = video_source.getvalue() if hasattr(video_source, "getvalue") else video_source.read()

        temp_dir = "./resources/temp_video"
        os.makedirs(temp_dir, exist_ok=True)
        import time
        tmp_path = os.path.join(temp_dir, f"cctv_{int(time.time())}{suffix}")

        with open(tmp_path, "wb") as f:
            f.write(video_bytes)

        with st.spinner("📹 Running automated frame-by-frame multi-face scanning..."):
            alerts, stats = scan_video_stream(
                video_path=tmp_path,
                user=user,
                frame_skip=frame_skip,
                distance_threshold=dist_thresh
            )

        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 Surveillance Diagnostic & Match Log")

        # Render Diagnostics Summary Grid
        st.markdown(
            f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 1.2rem; font-size: 0.88rem;">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center;">
                    <div style="background: #ffffff; padding: 0.6rem; border-radius: 8px; border: 1px solid #cbd5e1;">
                        <div style="font-size: 0.75rem; color: #64748b;">Sampled Frames</div>
                        <div style="font-weight: 800; color: #0f172a; font-size: 1.1rem;">{stats['total_frames']}</div>
                    </div>
                    <div style="background: #ffffff; padding: 0.6rem; border-radius: 8px; border: 1px solid #cbd5e1;">
                        <div style="font-size: 0.75rem; color: #64748b;">Faces Detected</div>
                        <div style="font-weight: 800; color: #1d4ed8; font-size: 1.1rem;">{stats['faces_detected']}</div>
                    </div>
                    <div style="background: #ffffff; padding: 0.6rem; border-radius: 8px; border: 1px solid #cbd5e1;">
                        <div style="font-size: 0.75rem; color: #64748b;">Closest Distance</div>
                        <div style="font-weight: 800; color: {'#10b981' if stats['min_distance'] and stats['min_distance'] <= dist_thresh else '#ef4444'}; font-size: 1.1rem;">
                            {stats['min_distance'] if stats['min_distance'] is not None else 'N/A'}
                        </div>
                    </div>
                    <div style="background: #ffffff; padding: 0.6rem; border-radius: 8px; border: 1px solid #cbd5e1;">
                        <div style="font-size: 0.75rem; color: #64748b;">DB Missing Records</div>
                        <div style="font-weight: 800; color: #0f172a; font-size: 1.1rem;">{stats['db_cases_count']}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if not alerts:
            st.warning("ℹ️ **No Match Triggered at Current Distance Threshold:**")
            if stats["min_distance"] is not None:
                st.info(
                    f"🔍 **AI Diagnostic Insight:** Detected face(s) in video with closest match distance of **`{stats['min_distance']}`** "
                    f"(Target Record: *{stats['min_distance_case']}*).\n\n"
                    f"💡 **Adjustment Tip:** Your *Match Sensitivity Distance* slider is currently set to **`{dist_thresh:.2f}`** (too strict).\n"
                    f"👉 **Increase the slider to `{max(2.5, stats['min_distance'] + 0.2):.1f}` or higher** and click **Start CCTV Surveillance Scan** to trigger the match alert!"
                )
            elif stats["faces_detected"] == 0:
                st.info("ℹ️ No clear faces detected in sampled video frames. Try setting *Frame Sampling Frequency* to `1` or `2` for denser sampling.")
            elif stats["db_cases_count"] == 0:
                st.info("ℹ️ No active missing person records found in database to compare against. Please register a missing person first.")
        else:
            st.success(f"🎉 **ALERT TRIGGERED:** Detected **{len(alerts)}** potential match event(s) in video footage!")
            
            for idx, alert in enumerate(alerts):
                st.markdown(
                    f"""
                    <div style="background: #fff5f5; border: 1.5px solid #fca5a5; border-radius: 14px; padding: 1.2rem; margin-bottom: 1.2rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.2rem; font-weight: 800; color: #991b1b;">
                                🚨 CCTV MATCH DETECTED: {alert['name']}
                            </div>
                            <div style="background: #fee2e2; color: #991b1b; padding: 4px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                                TIMESTAMPS: {alert['timestamp']} ({alert['timestamp_sec']}s) &nbsp;·&nbsp; CONFIDENCE: {alert['confidence']}%
                            </div>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

                snap_col, info_col = st.columns([1, 2], gap="medium")

                with snap_col:
                    try:
                        st.image(alert['snapshot_path'], use_container_width=True, caption=f"CCTV Frame @ {alert['timestamp']}")
                    except Exception:
                        st.caption("Snapshot unavailable")

                with info_col:
                    st.markdown(
                        f"""
                        <div style="font-size: 0.9rem; color: #334155; line-height: 1.7;">
                            <div><strong>Matched Person:</strong> {alert['name']}</div>
                            <div><strong>Registered Case ID:</strong> <code>{alert['case_id']}</code></div>
                            <div><strong>Last Seen Location:</strong> {alert['last_seen']} ({alert['city']})</div>
                            <div><strong>Spatial Euclidean Distance:</strong> <code>{alert['distance']}</code> (Threshold: {dist_thresh})</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
