import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render_current_weather(current_data, unit_label="°C", wind_label="m/s"):
    """Renders sleek, premium telemetry panels for Overah Core."""
    main_metrics = current_data["main"]
    wind = current_data["wind"]
    weather = current_data["weather"][0]
    
    temp = main_metrics["temp"]
    feels_like = main_metrics["feels_like"]
    humidity = main_metrics["humidity"]
    wind_speed = wind["speed"]
    condition = weather["description"].title()
    icon_code = weather["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

    # Topline Condition Banner (Fixed string quotation syntax error here)
    st.markdown(
        f"<div style='background: linear-gradient(90deg, #121620 0%, #0b0d12 100%); padding: 15px 20px; "
        f"border-left: 4px solid #00ffcc; border-radius: 8px; margin-bottom: 25px;'>"
        f"<p style='margin:0; font-size: 14px; color: #9ca3af; text-transform: uppercase; letter-spacing: 2px;'>System Status</p>"
        f"<h2 style='margin:0; color: #ffffff; font-weight: 700;'>{condition}</h2>"
        f"</div>", 
        unsafe_allow_html=True
    )
    
    # Primary Data Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"<div style='background-color: #121620; padding: 20px; border-radius: 8px; border: 1px solid #1f2937; text-align: center;'> "
            f"<p style='color: #9ca3af; margin: 0; font-size: 13px; text-transform: uppercase;'>Thermal Core</p>"
            f"<h1 style='color: #00ffcc; margin: 10px 0; font-family: monospace;'>{round(temp)}{unit_label}</h1>"
            f"<p style='color: #6b7280; margin: 0; font-size: 12px;'>Feels like: {round(feels_like)}{unit_label}</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div style='background-color: #121620; padding: 20px; border-radius: 8px; border: 1px solid #1f2937; text-align: center;'> "
            f"<p style='color: #9ca3af; margin: 0; font-size: 13px; text-transform: uppercase;'>Atmospheric Moisture</p>"
            f"<h1 style='color: #38bdf8; margin: 10px 0; font-family: monospace;'>{humidity}%</h1>"
            f"<p style='color: #6b7280; margin: 0; font-size: 12px;'>Condensation Risk: Low</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"<div style='background-color: #121620; padding: 20px; border-radius: 8px; border: 1px solid #1f2937; text-align: center;'> "
            f"<p style='color: #9ca3af; margin: 0; font-size: 13px; text-transform: uppercase;'>Vector Wind Speed</p>"
            f"<h1 style='color: #a78bfa; margin: 10px 0; font-family: monospace;'>{wind_speed} <span style='font-size:14px;'>{wind_label}</span></h1>"
            f"<p style='color: #6b7280; margin: 0; font-size: 12px;'>Directional Vector Flow</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"<div style='background-color: #121620; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; text-align: center; min-height: 128px;'>"
            f"<p style='color: #9ca3af; margin: 0; font-size: 13px; text-transform: uppercase;'>Visual Feed</p>"
            f"<img src='{icon_url}' style='width: 65px; margin: 0 auto; display: block;' />"
            f"</div>", 
            unsafe_allow_html=True
        )

def process_and_graph_forecast(forecast_data, unit_label="°C", wind_label="m/s", items_to_show=8):
    """Generates an error-free multi-tab premium layout for modern data analysis."""
    records = []
    for item in forecast_data["list"]:
        dt_obj = datetime.fromtimestamp(item["dt"])
        records.append({
            "Time": dt_obj.strftime("%I:%M %p"),
            "Temperature": item["main"]["temp"],
            "Humidity": item["main"]["humidity"],
            "Wind Speed": item["wind"]["speed"],
            "Condition": item["weather"][0]["main"],
            "Icon": item["weather"][0]["icon"],
            "DateLabel": dt_obj.strftime("%A, %b %d")
        })
        
    df = pd.DataFrame(records).head(items_to_show)

    st.markdown("<br><h3 style='color: #ffffff; font-weight:600;'>📊 Core Environmental Analytics Suite</h3>", unsafe_allow_html=True)
    
    # Modern Analytical Sub-Tabs
    tab_temp, tab_humid, tab_wind = st.tabs(["🌡️ Thermal Profile", "💧 Moisture Matrix", "💨 Kinetic Vector Flow"])
    
    with tab_temp:
        fig_temp = px.line(df, x="Time", y="Temperature", markers=True, text=[f"{round(t)}{unit_label}" for t in df["Temperature"]])
        fig_temp.update_traces(line=dict(color="#00ffcc", width=3, shape="spline"), marker=dict(size=8, color="#0b0d12", line=dict(width=2, color="#00ffcc")), textposition="top center")
        fig_temp.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#121620", margin=dict(l=40, r=20, t=15, b=15), height=280)
        fig_temp.update_xaxes(showgrid=False)
        fig_temp.update_yaxes(showgrid=True, gridcolor="#1f2937", title_text=f"Temperature ({unit_label})")
        st.plotly_chart(fig_temp, use_container_width=True)
        
    with tab_humid:
        fig_humid = px.bar(df, x="Time", y="Humidity")
        fig_humid.update_traces(marker_color="rgba(56, 189, 248, 0.4)", marker_line_color="#38bdf8", marker_line_width=1.5)
        fig_humid.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#121620", margin=dict(l=40, r=20, t=15, b=15), height=280)
        fig_humid.update_xaxes(showgrid=False)
        fig_humid.update_yaxes(showgrid=True, gridcolor="#1f2937", range=[0, 100], title_text="Humidity (%)")
        st.plotly_chart(fig_humid, use_container_width=True)
        
    with tab_wind:
        fig_wind = px.area(df, x="Time", y="Wind Speed")
        fig_wind.update_traces(line_color="#a78bfa", fillcolor="rgba(167, 139, 250, 0.1)")
        fig_wind.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#121620", margin=dict(l=40, r=20, t=15, b=15), height=280)
        fig_wind.update_xaxes(showgrid=False)
        fig_wind.update_yaxes(showgrid=True, gridcolor="#1f2937", title_text=f"Wind Speed ({wind_label})")
        st.plotly_chart(fig_wind, use_container_width=True)

    # 5-Day Outlook Render Cards
    st.markdown("<br><h3 style='color: #ffffff; font-weight:600;'>🔮 5-Day Predictive Core Outlook</h3>", unsafe_allow_html=True)
    df_all = pd.DataFrame(records)
    daily_df = df_all.drop_duplicates(subset=["DateLabel"], keep="first")
    
    cols = st.columns(len(daily_df))
    for index, (_, row) in enumerate(daily_df.iterrows()):
        with cols[index]:
            st.markdown(
                f"<div style='background-color: #121620; padding: 15px; border-radius: 8px; border: 1px solid #1f2937; text-align: center;'>"
                f"<p style='margin: 0; font-size: 13px; color: #9ca3af; font-weight: 600;'>{row['DateLabel'].split(',')[0]}</p>"
                f"<p style='margin: 0 0 10px 0; font-size: 11px; color: #6b7280;'>{row['DateLabel'].split(',')[1]}</p>"
                f"<img src='http://openweathermap.org/img/wn/{row['Icon']}.png' style='width: 45px; margin: 0 auto;' />"
                f"<h3 style='margin: 5px 0; color: #ffffff;'>{round(row['Temperature'])}{unit_label}</h3>"
                f"<span style='font-size: 11px; background-color: #1f2937; padding: 3px 8px; border-radius: 12px; color: #00ffcc;'>{row['Condition']}</span>"
                f"</div>", 
                unsafe_allow_html=True
            )