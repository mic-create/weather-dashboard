import streamlit as st
import os
from utils.api import get_coordinates, fetch_weather_data
from utils.ui_helpers import render_current_weather, process_and_graph_forecast

# 1. Advanced Page Configurations & Global Page Settings
st.set_page_config(
    page_title="Overah Core | Weather Intelligence", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Local Session Memory Stores for Bookmarks
if "favorites" not in st.session_state:
    st.session_state.favorites = ["New York", "London", "Tokyo"]

# 2. Sophisticated Overah Core Brand Theme Injection (CSS Overrides)
st.markdown("""
    <style>
    /* Premium Deep Matte Canvas Background */
    .stApp { background-color: #0b0d12; color: #f3f4f6; }
    
    /* Elegant Brand Accent Coloring for Primary Metrics */
    div[data-testid="stMetricValue"] { color: #00ffcc; font-weight: 700; font-family: 'Courier New', monospace; }
    
    /* Smooth Container Borders & Custom Sidebar Style */
    section[data-testid="stSidebar"] { background-color: #121620 !important; border-right: 1px solid #1f2937; }
    
    /* Clean Styling for Interactive Buttons */
    div.stButton > button:first-child {
        background-color: #1f2937; color: #ffffff; border: 1px solid #374151; transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #00ffcc; color: #0b0d12; border-color: #00ffcc; box-shadow: 0 0 10px rgba(0, 255, 204, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Responsive Header & Sophisticated Brand Integration
header_logo_col, header_text_col = st.columns([1, 12])

with header_logo_col:
    # Safely load the local logo asset if it exists, otherwise fall back to a placeholder icon
    if os.path.exists("logo.png"):
        st.image("logo.png", width=75)
    else:
        # High sophistication fallback graphic anchor
        st.markdown("<h1 style='margin:0; padding:0; color:#00ffcc;'>⚡</h1>", unsafe_allow_html=True)

with header_text_col:
    st.markdown(
        "<h1 style='margin:0; padding-top:5px; font-weight:800; letter-spacing:-1px;'>"
        "OVERAH <span style='color:#00ffcc; font-weight:300;'>CORE</span> "
        "<span style='font-size:20px; font-weight:200; color:#9ca3af;'>| Environmental Intelligence Suite</span>"
        "</h1>", 
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# 4. Sidebar Workspace Module (Favorite Management Layouts)
st.sidebar.markdown("<h2 style='color:#00ffcc; font-size:18px;'>⭐ BOOKMARKED HUBS</h2>", unsafe_allow_html=True)
selected_fav = st.sidebar.selectbox("Directly pipeline to monitored system hubs:", [""] + st.session_state.favorites)

st.sidebar.markdown("---")
st.sidebar.caption("🤖 Powered by **Overah Core Engine v2.1**\nReal-time telemetry streams active.")

# 5. Core Search Terminal Componentry 
with st.container():
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        default_search = selected_fav if selected_fav else "Lagos"
        city_input = st.text_input("System Location Target Query:", value=default_search, placeholder="Enter global tracking target...")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        search_clicked = st.button("Execute Telemetry Parse", use_container_width=True)

active_query = city_input

# 6. Live Pipeline Execution Engine
if active_query:
    with st.spinner(f"Establishing downstream telemetry links for '{active_query}'..."):
        geo_data = get_coordinates(active_query)
        
        if geo_data:
            # Modern localization structural anchor
            st.markdown(f"### 📍 Monitoring Station: {geo_data['name'].upper()} [{geo_data['country']}]")
            
            # Sophisticated Bookmark Action Controls
            col_fav_btn, _ = st.columns([2, 3])
            with col_fav_btn:
                if geo_data['name'] not in st.session_state.favorites:
                    if st.button(f"🔒 Pin {geo_data['name']} to Systems Hub"):
                        st.session_state.favorites.append(geo_data['name'])
                        st.rerun()
                else:
                    if st.button(f"🔓 Sever {geo_data['name']} Link"):
                        st.session_state.favorites.remove(geo_data['name'])
                        st.rerun()

            st.markdown("<hr style='margin:10px 0; border-color:#1f2937;' />", unsafe_allow_html=True)

            # Gather Live Datasets
            current, forecast = fetch_weather_data(geo_data["lat"], geo_data["lon"])
            
            if current and forecast:
                render_current_weather(current)
                st.markdown("<br>", unsafe_allow_html=True)
                process_and_graph_forecast(forecast)
        else:
            st.error("Target identification failure. Coordinate node mapping unsuccessful.")