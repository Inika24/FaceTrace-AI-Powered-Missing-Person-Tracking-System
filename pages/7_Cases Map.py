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

ui_theme.render_header(
    title="Cases Density by City — GIS Map",
    subtitle="Geographic visualization of missing person cases and resolved sightings mapped across Indian cities",
    badge="GIS LOCATION ANALYTICS",
    icon="🗺️"
)

try:
    import folium
    from streamlit_folium import st_folium
except ImportError:
    st.error("Map rendering component loading...")
    st.stop()

CITY_COORDS = {
    "Delhi": (28.6139, 77.2090),
    "New Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Kanpur": (26.4499, 80.3319),
    "Nagpur": (21.1458, 79.0882),
    "Indore": (22.7196, 75.8577),
    "Thane": (19.2183, 72.9781),
    "Bhopal": (23.2599, 77.4126),
    "Visakhapatnam": (17.6868, 83.2185),
    "Patna": (25.5941, 85.1376),
    "Vadodara": (22.3072, 73.1812),
    "Surat": (21.1702, 72.8311),
    "Noida": (28.5355, 77.3910),
    "Gurgaon": (28.4595, 77.0266),
    "Gurugram": (28.4595, 77.0266),
    "Chandigarh": (30.7333, 76.7794),
    "Coimbatore": (11.0168, 76.9558),
    "Kochi": (9.9312, 76.2673),
    "Tiruppur": (11.1085, 77.3411),
    "Avinashi": (11.1928, 77.2687),
    "Agra": (27.1767, 78.0081),
    "Varanasi": (25.3176, 82.9739),
    "Meerut": (28.9845, 77.7064),
    "Raipur": (21.2514, 81.6296),
    "Ranchi": (23.3441, 85.3096),
    "Guwahati": (26.1445, 91.7362),
    "Jodhpur": (26.2389, 73.0243),
    "Amritsar": (31.6340, 74.8723),
    "Jabalpur": (23.1815, 79.9864),
    "Haora": (22.5958, 88.2636),
    "Faridabad": (28.4089, 77.3178),
    "Unknown": (20.5937, 78.9629),
}

counts = db_queries.get_case_counts_by_city()

if not counts:
    st.info("ℹ️ No registered cases with city location data available yet.")
    st.stop()

# Build Map with OpenStreetMap tiles (No API key needed)
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="OpenStreetMap")

placed = 0
for city, data in counts.items():
    total = data["found"] + data["not_found"]
    coords = CITY_COORDS.get(city)
    if coords is None:
        city_lower = city.lower()
        for key, val in CITY_COORDS.items():
            if key.lower() == city_lower:
                coords = val
                break
    if coords is None:
        continue

    radius = max(8, min(40, total * 5))
    color = "#ef4444" if data["not_found"] > 0 else "#10b981"
    tooltip = (
        f"<b>{city}</b><br>"
        f"Total Cases: {total}<br>"
        f"Active Missing: {data['not_found']}<br>"
        f"Resolved/Found: {data['found']}"
    )
    folium.CircleMarker(
        location=coords,
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        tooltip=folium.Tooltip(tooltip),
    ).add_to(m)
    placed += 1

map_col, table_col = st.columns([3, 2], gap="medium")

with map_col:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st_folium(m, width="100%", height=520, returned_objects=[])

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
    st.markdown("</div>", unsafe_allow_html=True)

with table_col:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("📊 City Case Density Summary")
    rows = [
        {
            "City": city,
            "Total": d["found"] + d["not_found"],
            "Found": d["found"],
            "Not Found": d["not_found"],
        }
        for city, d in counts.items()
    ]

    df = pd.DataFrame(rows).sort_values("Total", ascending=False).reset_index(drop=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
