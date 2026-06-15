import streamlit as st
import os
from utils.api import get_coordinates, fetch_weather_data
from utils.ui_helpers import render_current_weather, process_and_graph_forecast

# 1. Page Configuration Setup
st.set_page_config(
    page_title="Overah Core | Climate Suite", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

if "favorites" not in st.session_state:
    st.session_state.favorites = ["Lagos", "London", "Houston"]

# 2. Strict UI Layout Styles Injector (Matching Dark/Teal Brand)
st.markdown("""
    <style>
    /* Premium Slate Matte Styling Layouts */
    .stApp { background-color: #0b0d12; color: #f3f4f6; }
    
    /* Clean Sidebar Separators */
    section[data-testid="stSidebar"] { background-color: #0e1118 !important; border-right: 1px solid #1f2937; }
    
    /* Input Form Accent Overrides */
    div[data-baseweb="input"] { background-color: #121620 !important; border: 1px solid #1f2937 !important; border-radius: 6px !important; }
    input { color: #ffffff !important; }
    
    /* Interactive Premium Styled Button Components */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00ffcc 0%, #0099ff 100%); 
        color: #0b0d12; font-weight: 700; border: none; border-radius: 6px; padding: 10px 20px; transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px); box-shadow: 0 4px 15px rgba(0, 255, 204, 0.4); color: #0b0d12;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Structural Brand Title Layout Header
header_logo_col, header_text_col = st.columns([1, 15])
with header_logo_col:
    # Use your matching green brand logo asset cleanly
    if os.path.exists("My Logo.png"):
        st.image("My Logo.png", width=65)
    else:
        st.markdown("<h1 style='margin:0; color:#00ffcc;'>⚡</h1>", unsafe_allow_html=True)

with header_text_col:
    st.markdown(
        "<h1 style='margin:0; padding-top:4px; font-weight:800; font-family: system-ui; letter-spacing:-0.5px;'>"
        "OVERAH <span style='color:#00ffcc; font-weight:300;'>CORE</span> "
        "<span style='font-size:16px; font-weight:300; color:#6b7280; vertical-align:middle; margin-left:10px;'>ENVIRONMENTAL INTELLIGENCE SYSTEM v2.5</span>"
        "</h1>", 
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# 4. Sidebar Station Tracking Layout Component
st.sidebar.markdown("<p style='color:#00ffcc; font-size:11px; font-weight:700; letter-spacing:1px; margin-bottom:5px;'>MONITORED NODES</p>", unsafe_allow_html=True)
selected_fav = st.sidebar.selectbox("Jump to pinned network hub:", [""] + st.session_state.favorites, label_visibility="collapsed")

st.sidebar.markdown("<br><br><hr style='border-color:#1f2937;'/>", unsafe_allow_html=True)
st.sidebar.caption("🔒 Secured Node Connection Active. All environmental inputs are calibrated automatically.")

# 5. Location Search Bar Componentry
with st.container():
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        default_search = selected_fav if selected_fav else "Lagos"
        city_input = st.text_input("Enter Target Station Location Key:", value=default_search, placeholder="Search city environmental arrays...", label_visibility="collapsed")
    with col_btn:
        search_clicked = st.button("EXECUTE ANALYSIS", use_container_width=True)

active_query = city_input

# 6. Main Visual Core Render Execution Data Pipeline
if active_query:
    with st.spinner("Decoding telemetry metrics from atmospheric array..."):
        geo_data = get_coordinates(active_query)
        
        if geo_data:
            # Layout Header for the Selected Monitoring Station
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

            # Core API calls and visual rendering sequence
            current, forecast = fetch_weather_data(geo_data["lat"], geo_data["lon"])
            if current and forecast:
                render_current_weather(current)
                process_and_graph_forecast(forecast)
        else:
            st.error("System Matrix Mapping Failure: Location coordinate target not identified.")