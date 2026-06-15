import streamlit as st
import os
from utils.api import get_coordinates, fetch_weather_data
from utils.ui_helpers import render_current_weather, process_and_graph_forecast

# Page Configuration Setup
st.set_page_config(
    page_title="Overah Intelligence | Enterprise Climate Suite", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

if "favorites" not in st.session_state:
    st.session_state.favorites = ["Lagos", "London", "Houston"]

# Core CSS Style Overrides
st.markdown("""
    <style>
    .stApp { background-color: #0b0d12; color: #f3f4f6; }
    section[data-testid="stSidebar"] { background-color: #0e1118 !important; border-right: 1px solid #1f2937; }
    div[data-baseweb="input"] { background-color: #121620 !important; border: 1px solid #1f2937 !important; border-radius: 6px !important; }
    input { color: #ffffff !important; }
    
    button[data-baseweb="tab"] { color: #9ca3af !important; font-size: 14px !important; }
    button[aria-selected="true"] { color: #00ffcc !important; font-weight: bold !important; border-bottom-color: #00ffcc !important; }
    
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00ffcc 0%, #0099ff 100%); 
        color: #0b0d12; font-weight: 700; border: none; border-radius: 6px; padding: 10px 20px; transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px); box-shadow: 0 4px 15px rgba(0, 255, 204, 0.4); color: #0b0d12;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- ENTERPRISE CONTROL SIDEBAR -----------------
st.sidebar.markdown("<p style='color:#00ffcc; font-size:14px; font-weight:700; letter-spacing:1px; margin-bottom:0;'>⚡ OVERAH CORE INTEL</p>", unsafe_allow_html=True)
st.sidebar.caption("Commercial Telemetry Console")
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Metric Unit Selector Configuration
unit_system = st.sidebar.radio("Core Metric Engine Selection:", ["Metric Engine (°C, m/s)", "Imperial Engine (°F, mph)"])
unit_param = "metric" if "Metric" in unit_system else "imperial"
u_label = "°C" if unit_param == "metric" else "°F"
w_label = "m/s" if unit_param == "metric" else "mph"

st.sidebar.markdown("<hr style='border-color:#1f2937; margin:12px 0;'/>", unsafe_allow_html=True)

# Data Lookahead Configuration
lookahead_intervals = st.sidebar.slider("Timeline Evaluation Rows:", min_value=4, max_value=12, value=8, step=1)

st.sidebar.markdown("<hr style='border-color:#1f2937; margin:12px 0;'/>", unsafe_allow_html=True)

# Bookmark Dropdown Selector
st.sidebar.markdown("<p style='color:#9ca3af; font-size:11px; font-weight:700; letter-spacing:1px; margin-bottom:5px;'>MONITORED STATIONS</p>", unsafe_allow_html=True)
selected_fav = st.sidebar.selectbox("Jump to network hub:", [""] + st.session_state.favorites, label_visibility="collapsed")

st.sidebar.markdown("<hr style='border-color:#1f2937; margin:12px 0;'/>", unsafe_allow_html=True)

# Enterprise Operational Safety Monitor Widget
st.sidebar.markdown("<p style='color:#ffffff; font-size:12px; font-weight:600;'>🚨 CORE RISK MONITOR</p>", unsafe_allow_html=True)
# -----------------------------------------------------------

# Primary Top Header Brand Setup
header_logo_col, header_text_col = st.columns([1, 15])
with header_logo_col:
    if os.path.exists("My Logo.png"):
        st.image("My Logo.png", width=65)
    else:
        st.markdown("<h1 style='margin:0; color:#00ffcc;'>⚡</h1>", unsafe_allow_html=True)

with header_text_col:
    st.markdown(
        "<h1 style='margin:0; padding-top:4px; font-weight:800; font-family: system-ui; letter-spacing:-0.5px; color:#ffffff;'>"
        "OVERAH <span style='color:#0055ff; font-weight:900;'>CORE</span> "
        "<span style='font-size:14px; font-weight:400; color:#4b5563; vertical-align:middle; margin-left:10px;'>ENVIRONMENTAL DECISION SUPPORT SYSTEM v3.0</span>"
        "</h1>", 
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Target Tracking Input Box
with st.container():
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        default_search = selected_fav if selected_fav else "Lagos"
        city_input = st.text_input("Enter Target Station Location Key:", value=default_search, placeholder="Search city environmental arrays...", label_visibility="collapsed")
    with col_btn:
        search_clicked = st.button("EXECUTE ANALYSIS", use_container_width=True)

active_query = city_input

if active_query:
    with st.spinner("Decoding telemetry metrics from atmospheric array..."):
        geo_data = get_coordinates(active_query)
        
        if geo_data:
            col_title, col_fav_action = st.columns([4, 1])
            with col_title:
                st.markdown(f"<h2 style='margin:0; font-weight:600;'>📍 Node: {geo_data['name']}, {geo_data['country']}</h2>", unsafe_allow_html=True)
            
            with col_fav_action:
                if geo_data['name'] not in st.session_state.favorites:
                    if st.button("➕ Pin Station", use_container_width=True):
                        st.session_state.favorites.append(geo_data['name'])
                        st.rerun()
                else:
                    if st.button("❌ Remove Station", use_container_width=True):
                        st.session_state.favorites.remove(geo_data['name'])
                        st.rerun()

            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

            current, forecast = fetch_weather_data(geo_data["lat"], geo_data["lon"], units=unit_param)
            if current and forecast:
                # Dynamic Sidebar Injection for Risk Analysis
                cur_wind = current["wind"]["speed"]
                cur_temp = current["main"]["temp"]
                
                if cur_wind > 15 or cur_temp > 35 or cur_temp < 5:
                    st.sidebar.error(f"CRITICAL HAZARD ASSIGNED\nHigh environmental disruption limits breached at tracking node.")
                else:
                    st.sidebar.success("STATION SCAN: STABLE\nNo business risk vectors flagged across local tracking grids.")
                
                render_current_weather(current, unit_label=u_label, wind_label=w_label)
                process_and_graph_forecast(forecast, unit_label=u_label, wind_label=w_label, items_to_show=lookahead_intervals)
        else:
            st.error("System Matrix Mapping Failure: Location coordinate target not identified.")