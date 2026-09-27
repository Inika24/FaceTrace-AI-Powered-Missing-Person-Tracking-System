import urllib.parse
import urllib.request
import json
import streamlit as st

# Built-in fast lookup dictionary for major cities, states, and countries
LOCATION_COORDS = {
    # Indian Cities
    "Chennai": (13.0827, 80.2707),
    "Tiruppur": (11.1085, 77.3411),
    "Avinashi": (11.1928, 77.2687),
    "Coimbatore": (11.0168, 76.9558),
    "Madurai": (9.9252, 78.1198),
    "Salem": (11.6643, 78.1460),
    "Trichy": (10.7905, 78.7047),
    "Tiruchirappalli": (10.7905, 78.7047),
    "Erode": (11.3410, 77.7172),
    "Vellore": (12.9165, 79.1325),
    "Thanjavur": (10.7870, 79.1378),
    "Tirunelveli": (8.7139, 77.7567),
    "Kanchipuram": (12.8342, 79.7036),
    "Kanyakumari": (8.0883, 77.5385),
    "Bengaluru": (12.9716, 77.5946),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Thane": (19.2183, 72.9781),
    "Nagpur": (21.1458, 79.0882),
    "Delhi": (28.6139, 77.2090),
    "New Delhi": (28.6139, 77.2090),
    "Noida": (28.5355, 77.3910),
    "Gurgaon": (28.4595, 77.0266),
    "Gurugram": (28.4595, 77.0266),
    "Kolkata": (22.5726, 88.3639),
    "Ahmedabad": (23.0225, 72.5714),
    "Surat": (21.1702, 72.8311),
    "Vadodara": (22.3072, 73.1812),
    "Jaipur": (26.9124, 75.7873),
    "Jodhpur": (26.2389, 73.0243),
    "Lucknow": (26.8467, 80.9462),
    "Kanpur": (26.4499, 80.3319),
    "Varanasi": (25.3176, 82.9739),
    "Agra": (27.1767, 78.0081),
    "Patna": (25.5941, 85.1376),
    "Bhopal": (23.2599, 77.4126),
    "Indore": (22.7196, 75.8577),
    "Visakhapatnam": (17.6868, 83.2185),
    "Kochi": (9.9312, 76.2673),
    "Trivandrum": (8.5241, 76.9366),
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Chandigarh": (30.7333, 76.7794),
    "Amritsar": (31.6340, 74.8723),
    "Guwahati": (26.1445, 91.7362),
    "Raipur": (21.2514, 81.6296),
    "Ranchi": (23.3441, 85.3096),
    "Dehradun": (30.3165, 78.0322),
    "Shimla": (31.1048, 77.1734),

    # Indian States & Union Territories
    "Tamil Nadu": (11.1271, 78.6569),
    "Kerala": (10.8505, 76.2711),
    "Karnataka": (15.3173, 75.7139),
    "Andhra Pradesh": (15.9129, 79.7400),
    "Telangana": (18.1124, 79.0193),
    "Maharashtra": (19.7515, 75.7139),
    "Goa": (15.2993, 74.1240),
    "Gujarat": (22.2587, 71.1924),
    "Rajasthan": (27.0238, 74.2179),
    "Uttar Pradesh": (26.8467, 80.9462),
    "Madhya Pradesh": (22.9734, 78.6569),
    "Bihar": (25.0961, 85.3131),
    "West Bengal": (22.9868, 87.8550),
    "Odisha": (20.9517, 85.0985),
    "Punjab": (31.1471, 75.3412),
    "Haryana": (29.0588, 76.0856),
    "Assam": (26.2006, 92.9376),
    "Delhi NCR": (28.6139, 77.2090),

    # International Cities
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Tokyo": (35.6762, 139.6503),
    "Dubai": (25.2048, 55.2708),
    "Singapore": (1.3521, 103.8198),
    "Sydney": (33.8688, 151.2093),
    "Chicago": (41.8781, -87.6298),
    "Los Angeles": (34.0522, -118.2437),
    "Toronto": (43.6532, -79.3832),
    "San Francisco": (37.7749, -122.4194),
    "Berlin": (52.5200, 13.4050),

    # Major Countries
    "India": (20.5937, 78.9629),
    "United States": (37.0902, -95.7129),
    "USA": (37.0902, -95.7129),
    "United Kingdom": (55.3781, -3.4360),
    "UK": (55.3781, -3.4360),
    "Canada": (56.1304, -106.3468),
    "Australia": (-25.2744, 133.7751),
    "Germany": (51.1657, 10.4515),
    "France": (46.2276, 2.2137),
    "Japan": (36.2048, 138.2529),
    "United Arab Emirates": (23.4241, 53.8478),
    "UAE": (23.4241, 53.8478),
    "South Africa": (-30.5595, 22.9375),
    "Brazil": (-14.2350, -51.9253),
    "Unknown": (20.5937, 78.9629)
}

@st.cache_data(ttl=86400, show_spinner=False)
def get_location_coords(location_name: str):
    """
    Resolve coordinates (lat, lon) for ANY City, State, or Country worldwide.
    Tries built-in dictionary first, fallback to dynamic Nominatim Geocoding API.
    """
    if not location_name or location_name.strip() == "" or location_name.lower() == "unknown":
        return (20.5937, 78.9629)

    loc_str = location_name.strip()

    # 1. Built-in Exact or Case-Insensitive Match
    if loc_str in LOCATION_COORDS:
        return LOCATION_COORDS[loc_str]

    for key, coords in LOCATION_COORDS.items():
        if key.lower() == loc_str.lower():
            return coords

    # 2. Dynamic Nominatim OpenStreetMap Geocoding Fallback
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(loc_str)}"
        req = urllib.request.Request(url, headers={"User-Agent": "MissingPersonAIApp/1.0"})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0:
                return (float(data[0]["lat"]), float(data[0]["lon"]))
    except Exception:
        pass

    # Default fallback to India center if unresolvable
    return (20.5937, 78.9629)

def render_english_map(counts_dict: dict, height: int = 500):
    """
    Render Folium GIS map using 100% Free English Esri World Street Map tiles (No API key needed).
    Supports Cities, States, and Countries.
    """
    import folium
    from streamlit_folium import st_folium

    # Esri World Street Map (Free English Labels, No API Key Required)
    tiles_url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    attr = "Esri, HERE, Garmin, USGS, NGA, EPA, USDA, NPS"

    m = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=4,
        tiles=tiles_url,
        attr=attr
    )

    if counts_dict:
        for loc, data in counts_dict.items():
            total = data["found"] + data["not_found"]
            coords = get_location_coords(loc)
            if not coords:
                continue

            radius = max(8, min(40, total * 6))
            color = "#ef4444" if data["not_found"] > 0 else "#10b981"
            tooltip = (
                f"<b>📍 Location: {loc}</b><br>"
                f"Total Cases: {total}<br>"
                f"Active Missing: {data['not_found']}<br>"
                f"Resolved / Found: {data['found']}"
            )

            folium.CircleMarker(
                location=coords,
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.65,
                tooltip=folium.Tooltip(tooltip),
            ).add_to(m)

    st_folium(m, width="100%", height=height, returned_objects=[])
