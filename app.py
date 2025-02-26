import streamlit as st
import requests
import time
from datetime import datetime

# OpenWeather API Key
API_KEY = "e0bf924da45b0002b44be649d164bf8a"  # Replace with a valid API key

# Function to fetch current weather data
def get_weather(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

# Function to fetch weekly weather forecast
def get_weekly_forecast(lat, lon, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "cnt": 7}
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

# Function to get an icon based on weather condition
def get_weather_icon(weather_desc):
    icons = {
        "clear": "☀️",
        "clouds": "☁️",
        "rain": "🌧️",
        "snow": "❄️",
        "thunderstorm": "⛈️",
        "drizzle": "🌦️",
        "mist": "🌫️"
    }
    for key in icons.keys():
        if key in weather_desc.lower():
            return icons[key]
    return "🌍"

# Function to get a weather-based quote
def get_weather_quote(weather_desc):
    quotes = {
        "clear": "☀️ The sun is shining, and so should you! Enjoy the beautiful day. 🌞",
        "clouds": "☁️ Life is like a cloudy day—there’s always sunshine behind the clouds! 🌥️",
        "rain": "🌧️ Let the rain remind you that growth often comes after a storm. ☔",
        "snow": "❄️ Just like every snowflake is unique, so are you! Keep shining. ⛄",
        "thunderstorm": "⛈️ Storms don’t last forever. Stay strong, the sun will shine soon! 🌤️",
        "drizzle": "💧 Small drops create mighty oceans—every little effort counts! 🌦️",
        "mist": "🌫️ Even in the foggiest moments, trust that clarity is ahead. 🌁"
    }
    for key in quotes.keys():
        if key in weather_desc.lower():
            return quotes[key]
    return "No matter the weather, make the most of today! 😊"

# Function to format date
def format_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%A, %b %d')

# Main function to run the app
def main():
    st.set_page_config(page_title="Weather Forecast", page_icon="🌤️", layout="wide")

    # Custom Styling
    st.markdown("""
       <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .weather-card {
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            color: white;
            padding: 10px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 15px;
        }
        .forecast-card {
            background: linear-gradient(135deg, rgb(233, 85, 90), rgb(247, 171, 150));
            color: white;
            padding: 5px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.15);
            width: 100%;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🌤️ Weather Forecast App")
    st.markdown("Get real-time weather updates and a weekly forecast for any city.")

    city = st.text_input("🌍 Enter city name:", "Pakistan")

    if st.button("🔍 Get Weather Data"):
        with st.spinner("Fetching weather details... ⏳"):
            time.sleep(2)  # Simulating loading time
            weather_data = get_weather(city, API_KEY)

        if weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            weather_desc = weather_data['weather'][0]['description'].capitalize()
            wind_speed = weather_data['wind']['speed']
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            icon = get_weather_icon(weather_desc)
            quote = get_weather_quote(weather_desc)

            # Display current weather
            st.markdown(f"<div class='weather-card'>", unsafe_allow_html=True)
            st.markdown(f"## {icon} {city}")
            st.markdown(f"### {weather_desc}")
            col1, col2, col3 = st.columns(3)
            col1.metric(label="🌡️ Temperature", value=f"{temp}°C")
            col2.metric(label="💧 Humidity", value=f"{humidity}%")
            col3.metric(label="💨 Wind Speed", value=f"{wind_speed} m/s")
            st.markdown(f"</div>", unsafe_allow_html=True)
            st.info(quote)

            # Fetch weekly forecast
            weekly_forecast = get_weekly_forecast(lat, lon, API_KEY)

            if weekly_forecast:
                st.markdown("---")
                st.markdown("### 📅 Weekly Forecast")
                forecast_data = weekly_forecast["list"]

                # Create a dynamic layout based on the screen size
                num_cols = 4 if st.session_state.get("mobile_view") else 7  # 4 columns on mobile, 7 on desktop
                cols = st.columns(num_cols)

                for i, day_data in enumerate(forecast_data[:7]):  # Limit to 7 days
                    forecast_date = format_date(day_data["dt"])
                    forecast_temp = day_data["main"]["temp"]
                    min_temp = day_data["main"]["temp_min"]
                    max_temp = day_data["main"]["temp_max"]
                    forecast_desc = day_data["weather"][0]["description"].capitalize()
                    forecast_icon = get_weather_icon(forecast_desc)

                    with cols[i % num_cols]:  # Distribute elements across available columns
                        st.markdown(f"<div class='forecast-card'>", unsafe_allow_html=True)
                        st.markdown(f"**{forecast_date}**")
                        st.markdown(f"{forecast_icon}")
                        st.markdown(f"🌡️ **{forecast_temp}°C**")
                        st.markdown(f"🌡️ Min: {min_temp}°C | 🔥 Max: {max_temp}°C")
                        st.markdown(f"🌥️ {forecast_desc}")
                        st.markdown(f"</div>", unsafe_allow_html=True)
            else:
                st.error("❌ Failed to fetch weekly forecast. Please try again.")

        else:
            st.error("❌ Failed to fetch weather data. Please check the city name and try again.")

    # Copyright Message
    st.markdown("---")
    st.markdown("🔹 **Built with ❤️ by Ausaf Ul Islam** | Stay informed, stay inspired!")

if __name__ == "__main__":
    main()
