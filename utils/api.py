import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
# Using 5-day/3-hour forecast for broad free-tier compatibility, or adapt easily to One Call 3.0
WEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast" 
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_coordinates(city_name: str) -> dict:
    """Fetch latitude and longitude for a given city string."""
    if not API_KEY:
        st.error("API Key missing! Please configure it in the .env file.")
        return None
    
    params = {"q": city_name, "limit": 1, "appid": API_KEY}
    try:
        response = requests.get(GEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            return {"lat": data[0]["lat"], "lon": data[0]["lon"], "name": data[0]["name"], "country": data[0]["country"]}
        return None
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP Error occurred while geocoding: {http_err}")
    except requests.exceptions.ConnectionError:
        st.error("Network connection error. Check your internet connectivity.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    return None

def fetch_weather_data(lat: float, lon: float) -> tuple:
    """Fetches current conditions and forecast blocks matching lat/lon."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric" # Change to 'imperial' for Fahrenheit
    }
    try:
        current_res = requests.get(CURRENT_WEATHER_URL, params=params, timeout=10)
        current_res.raise_for_status()
        
        forecast_res = requests.get(WEATHER_URL, params=params, timeout=10)
        forecast_res.raise_for_status()
        
        return current_res.json(), forecast_res.json()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            st.error("Invalid API Key. Please verify your OpenWeather Account status.")
        else:
            st.error(f"API Error ({err.response.status_code}): failed to acquire datasets.")
    except Exception as e:
        st.error(f"Data transmission failure: {e}")
    return None, None