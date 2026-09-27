import streamlit as st
import pandas as pd

from pages.helper import db_queries
from pages.helper import ui_theme

st.set_page_config(
    page_title="Cases Map • Missing Person AI",
    page_icon="🗺️",
    layout="wide"
)

ui_theme.inject_custom_theme()

from pages.helper import geo_utils

ui_theme.render_header(
    title="Geographic Case Density — GIS Map",
    subtitle="Interactive location tracking mapped across Cities, States, and Countries",
    badge="GIS LOCATION ANALYTICS",
    icon="🗺️"
)

counts = db_queries.get_case_counts_by_city()

if not counts:
    st.info("ℹ️ No registered cases with location data available yet.")
    st.stop()

map_col, table_col = st.columns([3, 2], gap="medium")

with map_col:
    geo_utils.render_english_map(counts, height=500)
    st.markdown(
        """
        <div class="legend-box" style="font-size: 0.85rem; color: #64748b; margin-top: 10px; display: flex; gap: 15px; align-items: center;">
            <span><strong style="color: #ef4444;">🔴 Has Unresolved Cases</strong></span>
            <span><strong style="color: #10b981;">🟢 All Cases Resolved</strong></span>
            <span><em>Circle radius proportional to case volume</em></span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with table_col:
    st.subheader("📊 Location Case Density Summary")
    st.caption("Includes City, State, and Country Records")
    rows = [
        {
            "Location (City / State / Country)": city,
            "Total": d["found"] + d["not_found"],
            "Found": d["found"],
            "Not Found": d["not_found"],
        }
        for city, d in counts.items()
    ]

    df = pd.DataFrame(rows).sort_values("Total", ascending=False).reset_index(drop=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

