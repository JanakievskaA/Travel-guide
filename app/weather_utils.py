import requests
import streamlit as st
from config import OPENWEATHER_API_KEY, CITY_COORDINATES, SUPPORTED_CITIES

# Average monthly temperatures (°C) and conditions for each city
# This serves as fallback when API is not available
MONTHLY_WEATHER_DATA = {
    "Paris": {
        "January": {"temp": 5, "condition": "Cold & Rainy", "rain_days": 10},
        "February": {"temp": 6, "condition": "Cold & Rainy", "rain_days": 9},
        "March": {"temp": 10, "condition": "Cool & Variable", "rain_days": 10},
        "April": {"temp": 13, "condition": "Mild & Pleasant", "rain_days": 9},
        "May": {"temp": 17, "condition": "Warm & Pleasant", "rain_days": 10},
        "June": {"temp": 20, "condition": "Warm & Sunny", "rain_days": 8},
        "July": {"temp": 23, "condition": "Hot & Sunny", "rain_days": 6},
        "August": {"temp": 23, "condition": "Hot & Sunny", "rain_days": 6},
        "September": {"temp": 19, "condition": "Warm & Pleasant", "rain_days": 7},
        "October": {"temp": 14, "condition": "Cool & Rainy", "rain_days": 9},
        "November": {"temp": 9, "condition": "Cold & Rainy", "rain_days": 10},
        "December": {"temp": 5, "condition": "Cold & Rainy", "rain_days": 10}
    },
    "Rome": {
        "January": {"temp": 8, "condition": "Cool & Rainy", "rain_days": 7},
        "February": {"temp": 9, "condition": "Cool & Variable", "rain_days": 7},
        "March": {"temp": 12, "condition": "Mild & Pleasant", "rain_days": 7},
        "April": {"temp": 15, "condition": "Warm & Pleasant", "rain_days": 7},
        "May": {"temp": 20, "condition": "Warm & Sunny", "rain_days": 5},
        "June": {"temp": 24, "condition": "Hot & Sunny", "rain_days": 3},
        "July": {"temp": 27, "condition": "Hot & Dry", "rain_days": 1},
        "August": {"temp": 27, "condition": "Hot & Dry", "rain_days": 2},
        "September": {"temp": 23, "condition": "Warm & Pleasant", "rain_days": 5},
        "October": {"temp": 18, "condition": "Mild & Rainy", "rain_days": 7},
        "November": {"temp": 13, "condition": "Cool & Rainy", "rain_days": 9},
        "December": {"temp": 9, "condition": "Cool & Rainy", "rain_days": 8}
    },
    "Madrid": {
        "January": {"temp": 6, "condition": "Cold & Dry", "rain_days": 4},
        "February": {"temp": 8, "condition": "Cool & Variable", "rain_days": 4},
        "March": {"temp": 11, "condition": "Mild & Pleasant", "rain_days": 4},
        "April": {"temp": 14, "condition": "Mild & Pleasant", "rain_days": 6},
        "May": {"temp": 18, "condition": "Warm & Pleasant", "rain_days": 5},
        "June": {"temp": 24, "condition": "Hot & Sunny", "rain_days": 2},
        "July": {"temp": 28, "condition": "Hot & Dry", "rain_days": 1},
        "August": {"temp": 28, "condition": "Hot & Dry", "rain_days": 1},
        "September": {"temp": 23, "condition": "Warm & Pleasant", "rain_days": 3},
        "October": {"temp": 16, "condition": "Mild & Pleasant", "rain_days": 5},
        "November": {"temp": 10, "condition": "Cool & Rainy", "rain_days": 5},
        "December": {"temp": 7, "condition": "Cold & Dry", "rain_days": 5}
    },
    "Berlin": {
        "January": {"temp": 1, "condition": "Cold & Snowy", "rain_days": 10},
        "February": {"temp": 2, "condition": "Cold & Dry", "rain_days": 8},
        "March": {"temp": 6, "condition": "Cool & Variable", "rain_days": 9},
        "April": {"temp": 10, "condition": "Cool & Variable", "rain_days": 8},
        "May": {"temp": 15, "condition": "Mild & Pleasant", "rain_days": 9},
        "June": {"temp": 18, "condition": "Warm & Pleasant", "rain_days": 10},
        "July": {"temp": 20, "condition": "Warm & Pleasant", "rain_days": 10},
        "August": {"temp": 20, "condition": "Warm & Pleasant", "rain_days": 9},
        "September": {"temp": 15, "condition": "Mild & Rainy", "rain_days": 8},
        "October": {"temp": 10, "condition": "Cool & Rainy", "rain_days": 8},
        "November": {"temp": 5, "condition": "Cold & Rainy", "rain_days": 9},
        "December": {"temp": 2, "condition": "Cold & Snowy", "rain_days": 10}
    },
    "Milan": {
        "January": {"temp": 3, "condition": "Cold & Foggy", "rain_days": 6},
        "February": {"temp": 6, "condition": "Cold & Variable", "rain_days": 5},
        "March": {"temp": 11, "condition": "Mild & Variable", "rain_days": 7},
        "April": {"temp": 15, "condition": "Mild & Rainy", "rain_days": 9},
        "May": {"temp": 19, "condition": "Warm & Pleasant", "rain_days": 10},
        "June": {"temp": 24, "condition": "Hot & Sunny", "rain_days": 7},
        "July": {"temp": 26, "condition": "Hot & Humid", "rain_days": 5},
        "August": {"temp": 26, "condition": "Hot & Humid", "rain_days": 6},
        "September": {"temp": 21, "condition": "Warm & Pleasant", "rain_days": 6},
        "October": {"temp": 15, "condition": "Cool & Foggy", "rain_days": 8},
        "November": {"temp": 9, "condition": "Cold & Foggy", "rain_days": 8},
        "December": {"temp": 4, "condition": "Cold & Foggy", "rain_days": 6}
    },
    "Lisbon": {
        "January": {"temp": 12, "condition": "Mild & Rainy", "rain_days": 8},
        "February": {"temp": 13, "condition": "Mild & Rainy", "rain_days": 7},
        "March": {"temp": 15, "condition": "Mild & Pleasant", "rain_days": 6},
        "April": {"temp": 17, "condition": "Warm & Pleasant", "rain_days": 6},
        "May": {"temp": 20, "condition": "Warm & Sunny", "rain_days": 4},
        "June": {"temp": 23, "condition": "Hot & Sunny", "rain_days": 2},
        "July": {"temp": 26, "condition": "Hot & Sunny", "rain_days": 1},
        "August": {"temp": 26, "condition": "Hot & Sunny", "rain_days": 1},
        "September": {"temp": 24, "condition": "Warm & Sunny", "rain_days": 3},
        "October": {"temp": 20, "condition": "Mild & Rainy", "rain_days": 6},
        "November": {"temp": 15, "condition": "Mild & Rainy", "rain_days": 8},
        "December": {"temp": 12, "condition": "Mild & Rainy", "rain_days": 8}
    },
    "Vienna": {
        "January": {"temp": 1, "condition": "Cold & Snowy", "rain_days": 8},
        "February": {"temp": 3, "condition": "Cold & Variable", "rain_days": 7},
        "March": {"temp": 7, "condition": "Cool & Variable", "rain_days": 8},
        "April": {"temp": 12, "condition": "Mild & Pleasant", "rain_days": 7},
        "May": {"temp": 17, "condition": "Warm & Pleasant", "rain_days": 9},
        "June": {"temp": 20, "condition": "Warm & Pleasant", "rain_days": 10},
        "July": {"temp": 23, "condition": "Warm & Sunny", "rain_days": 9},
        "August": {"temp": 22, "condition": "Warm & Sunny", "rain_days": 8},
        "September": {"temp": 17, "condition": "Mild & Pleasant", "rain_days": 7},
        "October": {"temp": 11, "condition": "Cool & Rainy", "rain_days": 7},
        "November": {"temp": 6, "condition": "Cold & Rainy", "rain_days": 8},
        "December": {"temp": 2, "condition": "Cold & Snowy", "rain_days": 8}
    },
    "Barcelona": {
        "January": {"temp": 10, "condition": "Mild & Pleasant", "rain_days": 4},
        "February": {"temp": 11, "condition": "Mild & Pleasant", "rain_days": 4},
        "March": {"temp": 13, "condition": "Mild & Pleasant", "rain_days": 5},
        "April": {"temp": 16, "condition": "Warm & Pleasant", "rain_days": 6},
        "May": {"temp": 19, "condition": "Warm & Sunny", "rain_days": 6},
        "June": {"temp": 23, "condition": "Hot & Sunny", "rain_days": 4},
        "July": {"temp": 26, "condition": "Hot & Sunny", "rain_days": 2},
        "August": {"temp": 26, "condition": "Hot & Humid", "rain_days": 4},
        "September": {"temp": 23, "condition": "Warm & Pleasant", "rain_days": 5},
        "October": {"temp": 19, "condition": "Mild & Rainy", "rain_days": 7},
        "November": {"temp": 14, "condition": "Mild & Rainy", "rain_days": 5},
        "December": {"temp": 11, "condition": "Mild & Pleasant", "rain_days": 5}
    },
    "London": {
        "January": {"temp": 5, "condition": "Cold & Rainy", "rain_days": 11},
        "February": {"temp": 5, "condition": "Cold & Rainy", "rain_days": 8},
        "March": {"temp": 8, "condition": "Cool & Variable", "rain_days": 9},
        "April": {"temp": 11, "condition": "Mild & Rainy", "rain_days": 9},
        "May": {"temp": 14, "condition": "Mild & Pleasant", "rain_days": 8},
        "June": {"temp": 18, "condition": "Warm & Pleasant", "rain_days": 8},
        "July": {"temp": 20, "condition": "Warm & Pleasant", "rain_days": 7},
        "August": {"temp": 20, "condition": "Warm & Pleasant", "rain_days": 8},
        "September": {"temp": 17, "condition": "Mild & Rainy", "rain_days": 8},
        "October": {"temp": 13, "condition": "Cool & Rainy", "rain_days": 10},
        "November": {"temp": 9, "condition": "Cold & Rainy", "rain_days": 10},
        "December": {"temp": 6, "condition": "Cold & Rainy", "rain_days": 10}
    },
    "Amsterdam": {
        "January": {"temp": 4, "condition": "Cold & Rainy", "rain_days": 12},
        "February": {"temp": 4, "condition": "Cold & Rainy", "rain_days": 10},
        "March": {"temp": 7, "condition": "Cool & Variable", "rain_days": 11},
        "April": {"temp": 10, "condition": "Cool & Variable", "rain_days": 9},
        "May": {"temp": 14, "condition": "Mild & Pleasant", "rain_days": 9},
        "June": {"temp": 17, "condition": "Warm & Pleasant", "rain_days": 9},
        "July": {"temp": 19, "condition": "Warm & Pleasant", "rain_days": 10},
        "August": {"temp": 19, "condition": "Warm & Pleasant", "rain_days": 10},
        "September": {"temp": 16, "condition": "Mild & Rainy", "rain_days": 10},
        "October": {"temp": 12, "condition": "Cool & Rainy", "rain_days": 11},
        "November": {"temp": 8, "condition": "Cold & Rainy", "rain_days": 13},
        "December": {"temp": 5, "condition": "Cold & Rainy", "rain_days": 12}
    },
}


def get_weather_emoji(condition: str) -> str:
    """Return emoji based on weather condition."""
    condition_lower = condition.lower()
    if "snow" in condition_lower:
        return "❄️"
    elif "rain" in condition_lower:
        return "🌧️"
    elif "hot" in condition_lower or "extremely" in condition_lower:
        return "🔥"
    elif "warm" in condition_lower and "sunny" in condition_lower:
        return "☀️"
    elif "warm" in condition_lower:
        return "🌤️"
    elif "humid" in condition_lower:
        return "💧"
    elif "cold" in condition_lower:
        return "🥶"
    elif "cool" in condition_lower:
        return "🌥️"
    elif "mild" in condition_lower or "pleasant" in condition_lower:
        return "😊"
    elif "dry" in condition_lower:
        return "🏜️"
    else:
        return "🌡️"


def get_clothing_recommendations(temp: int, condition: str) -> list:
    """Get clothing recommendations based on temperature and condition."""
    recommendations = []
    condition_lower = condition.lower()
    
    # Temperature-based recommendations
    if temp <= 5:
        recommendations.extend([
            "Heavy winter coat",
            "Warm scarf and gloves",
            "Thermal underwear",
            "Warm waterproof boots"
        ])
    elif temp <= 10:
        recommendations.extend([
            "Warm jacket or coat",
            "Light scarf",
            "Jeans or warm pants",
            "Comfortable closed shoes"
        ])
    elif temp <= 15:
        recommendations.extend([
            "Light jacket or sweater",
            "Long-sleeve shirts",
            "Pants or jeans",
            "Comfortable walking shoes"
        ])
    elif temp <= 22:
        recommendations.extend([
            "T-shirts and light shirts",
            "Shorts or light pants",
            "Comfortable sneakers",
            "Light jacket for evenings"
        ])
    elif temp <= 28:
        recommendations.extend([
            "Light, breathable clothing",
            "Shorts and summer dresses",
            "Sandals or breathable shoes",
            "Hat and sunglasses"
        ])
    else:
        recommendations.extend([
            "Very light, loose clothing",
            "Shorts and tank tops",
            "Sandals or flip-flops",
            "Wide-brimmed hat essential"
        ])
    
    # Condition-based additions
    if "rain" in condition_lower:
        recommendations.append("Umbrella (essential!)")
        recommendations.append("Waterproof jacket")

    if "humid" in condition_lower:
        recommendations.append("Moisture-wicking fabrics")
        recommendations.append("Antiperspirant")

    if "sunny" in condition_lower or "hot" in condition_lower:
        recommendations.append("Sunscreen SPF 50+")
        recommendations.append("UV-protection sunglasses")

    if "snow" in condition_lower:
        recommendations.append("Insulated waterproof gloves")
        recommendations.append("Snow boots with grip")
    
    return recommendations[:8]  # Return max 8 recommendations


def get_activity_recommendations(temp: int, condition: str, city: str) -> list:
    """Get activity recommendations based on weather."""
    recommendations = []
    condition_lower = condition.lower()
    
    # Indoor activities for bad weather
    if "rain" in condition_lower or "snow" in condition_lower or temp < 5 or temp > 35:
        recommendations.extend([
            "Perfect weather for museums",
            "Cozy café hopping",
            "Indoor shopping",
            "Theater or concert"
        ])

    # Outdoor activities for good weather
    if temp >= 15 and temp <= 28 and "rain" not in condition_lower:
        recommendations.extend([
            "Walking tours",
            "Parks and gardens",
            "Outdoor photography",
            "Al fresco dining"
        ])

    # Hot weather activities
    if temp > 28:
        recommendations.extend([
            "Swimming or beach",
            "Early morning sightseeing",
            "Evening activities",
            "Air-conditioned attractions"
        ])

    # Cool/mild weather
    if 10 <= temp <= 20:
        recommendations.extend([
            "Bike tours",
            "Hiking nearby",
            "Amusement parks",
            "Sunset watching"
        ])
    
    return recommendations[:6]


def get_weather_for_city(city: str, month: str) -> dict | None:
    """Get weather data for a city and month."""
    # Normalize month name
    month_normalized = month.strip().title()
    
    # Check if city is supported
    if city not in MONTHLY_WEATHER_DATA:
        return None
    
    city_weather = MONTHLY_WEATHER_DATA.get(city, {})
    
    if month_normalized not in city_weather:
        return None
    
    weather_data = city_weather[month_normalized]
    return {
        "city": city,
        "month": month_normalized,
        "temp": weather_data["temp"],
        "condition": weather_data["condition"],
        "rain_days": weather_data["rain_days"],
        "country": CITY_COORDINATES.get(city, {}).get("country", "")
    }


def display_weather_card(city: str, month: str):
    """Display a weather card for the specified city and month."""
    weather = get_weather_for_city(city, month)
    
    if not weather:
        st.info(f"Weather data not available for {city} in {month}")
        return
    
    emoji = get_weather_emoji(weather["condition"])
    temp = weather["temp"]
    condition = weather["condition"]
    rain_days = weather["rain_days"]
    
    # Weather card
    st.markdown("---")
    st.subheader(f"Weather Forecast: {city} in {weather['month']}")
    
    # Main weather display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Temperature",
            value=f"{temp}°C",
            delta=f"{round(temp * 9/5 + 32)}°F"
        )
    
    with col2:
        st.metric(
            label="Condition",
            value=f"{emoji} {condition}"
        )
    
    with col3:
        st.metric(
            label="Rainy Days",
            value=f"~{rain_days} days",
            delta="per month"
        )
    
    # Recommendations in expanders
    col_left, col_right = st.columns(2)

    with col_left:
        with st.expander("What to Pack", expanded=False):
            clothing = get_clothing_recommendations(temp, condition)
            for item in clothing:
                st.write(item)

    with col_right:
        with st.expander("Recommended Activities", expanded=False):
            activities = get_activity_recommendations(temp, condition, city)
            for activity in activities:
                st.write(activity)
    
    # Weather warning for extreme conditions
    if temp > 35:
        st.warning("⚠️ **Extreme Heat Warning**: Stay hydrated, avoid midday sun (12-4 PM), and seek air-conditioned spaces.")
    elif temp < 0:
        st.warning("⚠️ **Freezing Conditions**: Dress in layers, watch for ice, and limit outdoor exposure.")
    elif rain_days > 12:
        st.info("💡 **Rainy Season**: Consider flexible indoor activities and always carry an umbrella.")

