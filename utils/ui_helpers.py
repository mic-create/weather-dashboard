import streamlit as st
import pandas as pd
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
        st.markdown(
            f"<div style='background-color: #121620; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; text-align: center; min-height: 128px;'>"
            f"<p style='color: #9ca3af; margin: 0; font-size: 13px; text-transform: uppercase;'>Visual Feed</p>"
            f"<img src='{icon_url}' style='width: 65px; margin: 0 auto; display: block;' />"
            f"</div>", 
            unsafe_allow_html=True
        )

def process_and_graph_forecast(forecast_data):
    """Generates a sophisticated dual-axis layout combining line charts and column matrices."""
    records = []
    for item in forecast_data["list"]:
        dt_obj = datetime.fromtimestamp(item["dt"])
        records.append({
            "Timestamp": dt_obj,
            "Date": dt_obj.strftime("%A, %b %d"),
            "Time": dt_obj.strftime("%I:%M %p"),
            "Temperature": item["main"]["temp"],
            "Humidity": item["main"]["humidity"],
            "Condition": item["weather"][0]["main"],
            "Icon": item["weather"][0]["icon"]
        })
        
    df = pd.DataFrame(records)
    df_24h = df.head(8)  # Next 24 hours timeline matrix

    st.markdown("<br><h3 style='color: #ffffff; font-weight:600;'>📊 Dual-Axis Climate Correlation Analytics</h3>", unsafe_allow_html=True)
    
    fig = go.Figure()

    # Trace 1: Bar Matrix for Humidity (Mapped to the Right Y-Axis)
    fig.add_trace(go.Bar(
        x=df_24h["Time"],
        y=df_24h["Humidity"],
        name="Humidity (%)",
        yaxis="y2",
        marker=dict(color="rgba(56, 189, 248, 0.15)", line=dict(color="rgba(56, 189, 248, 0.4)", width=1)),
        hovertemplate="Atmospheric Humidity: %{y}%<extra></extra>"
    ))

    # Trace 2: Temperature Spline Curve (Mapped to the Left Y-Axis)
    fig.add_trace(go.Scatter(
        x=df_24h["Time"],
        y=df_24h["Temperature"],
        name="Temperature (°C)",
        mode="lines+markers+text",
        line=dict(color="#00ffcc", width=3, shape="spline"),
        marker=dict(size=8, color="#0b0d12", line=dict(color="#00ffcc", width=2)),
        text=[f"{round(val)}°C" for val in df_24h["Temperature"]],
        textposition="top center",
        textfont=dict(color="#ffffff", size=10, family="monospace"),
        hovertemplate="Thermal Reading: %{y:.1f}°C<extra></extra>"
    ))

    # Configuration for Dual-Axis Geometry Layout
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#121620",
        margin=dict(l=50, r=50, t=20, b=20),
        height=340,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        xaxis=dict(
            showgrid=False,
            color="#9ca3af"
        ),
        yaxis=dict(
            title="Temperature (°C)",
            titlefont=dict(color="#00ffcc", size=12),
            tickfont=dict(color="#00ffcc"),
            showgrid=True,
            gridcolor="#1f2937",
            zeroline=False
        ),
        yaxis2=dict(
            title="Humidity (%)",
            titlefont=dict(color="#38bdf8", size=12),
            tickfont=dict(color="#38bdf8"),
            showgrid=False,
            overlaying="y",
            side="right",
            range=[0, 100]
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # 5-Day Outlook Render Cards
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