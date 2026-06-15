import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def render_current_weather(current_data):
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

    # Topline Condition Banner
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
            f"<div style='background-color: #121620; padding: 20px; border-radius: 8px; border: 1px solid #1f2937; text-align: center;'>"
            f"<p style='color: #9ca3af; margin: 0; font-size: 13px; text-transform: uppercase;'>Thermal Core</p>"
            f"<h1 style='color: #00ffcc; margin: 10px 0; font-family: monospace;'>{round(temp)}°C</h1>"
            f"<p style='color: #6b7280; margin: 0; font-size: 12px;'>Feels like: {round(feels_like)}°C</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div style='background-color: #121620; padding: 20px; border-radius: 8px; border: 1px solid #1f2937; text-align: center;'>"
            f"<p style='color: #9ca3af; margin: 0; font-size: 13px; text-transform: uppercase;'>Atmospheric Moisture</p>"
            f"<h1 style='color: #38bdf8; margin: 10px 0; font-family: monospace;'>{humidity}%</h1>"
            f"<p style='color: #6b7280; margin: 0; font-size: 12px;'>Condensation Risk: Low</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"<div style='background-color: #121620; padding: 20px; border-radius: 8px; border: 1px solid #1f2937; text-align: center;'>"
            f"<p style='color: #9ca3af; margin: 0; font-size: 13px; text-transform: uppercase;'>Vector Wind Speed</p>"
            f"<h1 style='color: #a78bfa; margin: 10px 0; font-family: monospace;'>{wind_speed} <span style='font-size:16px;'>m/s</span></h1>"
            f"<p style='color: #6b7280; margin: 0; font-size: 12px;'>Directional Vector Flow</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
    with col4:
        # Diagnostic Visual Icon Card
        st.markdown(
            f"<div style='background-color: #121620; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; text-align: center; min-height: 128px;'>"
            f"<p style='color: #9ca3af; margin: 0; font-size: 13px; text-transform: uppercase;'>Visual Feed</p>"
            f"<img src='{icon_url}' style='width: 65px; margin: 0 auto; display: block;' />"
            f"</div>", 
            unsafe_allow_html=True
        )

def process_and_graph_forecast(forecast_data):
    """Generates elite interactive analytics trendlines and 5-day predictive tables."""
    records = []
    for item in forecast_data["list"]:
        dt_obj = datetime.fromtimestamp(item["dt"])
        records.append({
            "Timestamp": dt_obj,
            "Date": dt_obj.strftime("%A, %b %d"),
            "Time": dt_obj.strftime("%H:%M"),
            "Temperature": item["main"]["temp"],
            "Humidity": item["main"]["humidity"],
            "Condition": item["weather"][0]["main"],
            "Icon": item["weather"][0]["icon"]
        })
        
    df = pd.DataFrame(records)
    # Take the next 24 hours of data points (8 intervals of 3 hours) for the timeline
    df_24h = df.head(8)

    st.markdown("<br><h3 style='color: #ffffff; font-weight:600;'>📊 High-Fidelity Microclimate Timeline</h3>", unsafe_allow_html=True)
    
    # Premium Styled Plotly Graph Object
    fig = go.Figure()
    
    # Temperature Area Trace
    fig.add_trace(go.Scatter(
        x=df_24h["Timestamp"],
        y=df_24h["Temperature"],
        mode="lines+markers",
        name="Temperature (°C)",
        line=dict(color="#00ffcc", width=3, shape="spline"),
        marker=dict(size=8, color="#0b0d12", line=dict(color="#00ffcc", width=2)),
        hovertemplate="<b>%{x|%I:%M %p}</b><br>Thermal Metric: %{y:.1f}°C<extra></extra>"
    ))

    # Polished Graph Formatting Overrides
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#121620",
        margin=dict(l=40, r=20, t=10, b=10),
        height=320,
        hovermode="x unified",
        xaxis=dict(
            showgrid=True,
            gridcolor="#1f2937",
            tickformat="%I:%M %p",
            color="#9ca3af"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1f2937",
            title="Degrees Celsius",
            titlefont=dict(color="#9ca3af", size=11),
            color="#9ca3af"
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # Day-By-Day Condition Grid Layout
    st.markdown("<br><h3 style='color: #ffffff; font-weight:600;'>🔮 5-Day Predictive Core Outlook</h3>", unsafe_allow_html=True)
    daily_df = df.drop_duplicates(subset=["Date"], keep="first")
    
    cols = st.columns(len(daily_df))
    for index, (_, row) in enumerate(daily_df.iterrows()):
        with cols[index]:
            st.markdown(
                f"<div style='background-color: #121620; padding: 15px; border-radius: 8px; border: 1px solid #1f2937; text-align: center;'>"
                f"<p style='margin: 0; font-size: 13px; color: #9ca3af; font-weight: 600;'>{row['Date'].split(',')[0]}</p>"
                f"<p style='margin: 0 0 10px 0; font-size: 11px; color: #6b7280;'>{row['Date'].split(',')[1]}</p>"
                f"<img src='http://openweathermap.org/img/wn/{row['Icon']}.png' style='width: 45px; margin: 0 auto;' />"
                f"<h3 style='margin: 5px 0; color: #ffffff;'>{round(row['Temperature'])}°C</h3>"
                f"<span style='font-size: 11px; background-color: #1f2937; padding: 3px 8px; border-radius: 12px; color: #00ffcc;'>{row['Condition']}</span>"
                f"</div>", 
                unsafe_allow_html=True
            )