import os
import requests
import streamlit as st

# Retrieve the API key directly from Streamlit's native Secrets management
API_KEY = st.secrets.get("OPENWEATHER_API_KEY") if "OPENWEATHER_API_KEY" in st.secrets else os.getenv("OPENWEATHER_API_KEY")

GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast" 
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_coordinates(city_name: str) -> dict:
    """Fetch latitude and longitude for a given city string."""
    if not API_KEY:
        st.error("API Key missing! Please configure it in your Streamlit Secrets panel.")
        return None
    
    params = {"q": city_name, "limit": 1, "appid": API_KEY}
    try:
        response = requests.get(GEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            return {"lat": data[0]["lat"], "lon": data[0]["lon"], "name": data[0]["name"], "country": data[0]["country"]}
        return None
    except Exception as e:
        st.error(f"Geocoding connection error: {e}")
    return None

def fetch_weather_data(lat: float, lon: float) -> tuple:
    """Fetches current conditions and forecast blocks matching lat/lon."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        current_res = requests.get(CURRENT_WEATHER_URL, params=params, timeout=10)
        current_res.raise_for_status()
        
        forecast_res = requests.get(WEATHER_URL, params=params, timeout=10)
        forecast_res.raise_for_status()
        
        return current_res.json(), forecast_res.json()
    except Exception as e:
        st.error(f"Data transmission failure: {e}")
    return None, None