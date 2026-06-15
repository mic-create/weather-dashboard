import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render_current_weather(current_data):
    """Renders primary Hero metric block for target location."""
    temp = current_data["main"]["temp"]
    feels_like = current_data["main"]["feels_like"]
    humidity = current_data["main"]["humidity"]
    wind_speed = current_data["wind"]["speed"]
    weather_desc = current_data["weather"][0]["description"].title()
    icon_code = current_data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

    st.markdown(f"### Current Status: {weather_desc}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image(icon_url, width=80)
    with col2:
        st.metric(label="Temperature", value=f"{round(temp)}°C", delta=f"Feels like {round(feels_like)}°C")
    with col3:
        st.metric(label="Humidity", value=f"{humidity}%")
    with col4:
        st.metric(label="Wind Speed", value=f"{wind_speed} m/s")

def process_and_graph_forecast(forecast_data):
    """Extracts distinctive daily arrays & builds structural trend analysis."""
    records = []
    for item in forecast_data["list"]:
        dt_obj = datetime.fromtimestamp(item["dt"])
        records.append({
            "Date": dt_obj.strftime("%A\n%b %d"),
            "Time": dt_obj.strftime("%H:%M"),
            "Temp (°C)": item["main"]["temp"],
            "Humidity (%)": item["main"]["humidity"],
            "Icon": item["weather"][0]["icon"],
            "Desc": item["weather"][0]["main"]
        })
        
    df = pd.DataFrame(records)
    
    # Render Trend Line Charts
    st.markdown("### Temperature Timeline Trends")
    fig = px.line(df, x="Date", y="Temp (°C)", hover_data=["Time", "Desc"], markers=True)
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # Day-by-Day Conditions Forecast
    st.markdown("### Day-by-Day Conditions Forecast")
    daily_df = df.drop_duplicates(subset=["Date"], keep="first")
    
    cols = st.columns(len(daily_df))
    for index, (_, row) in enumerate(daily_df.iterrows()):
        with cols[index]:
            st.markdown(f"**{row['Date']}**")
            st.image(f"http://openweathermap.org/img/wn/{row['Icon']}.png", width=50)
            st.markdown(f"**{round(row['Temp (°C)'])}°C**")
            st.caption(f"{row['Desc']}")