import time
import streamlit as st
from cohere.errors import TooManyRequestsError
from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate
from config import COHERE_API_KEY, COHERE_MODEL, SUPPORTED_CITIES
from .map_utils import display_city_map, get_city_match
from .weather_utils import display_weather_card

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

llm = ChatCohere(model=COHERE_MODEL, cohere_api_key=COHERE_API_KEY)

prompt_template = PromptTemplate(
    input_variables=[
        "city", "days", "month", "language", "budget",
        "interests", "travel_pace", "travel_companions", "transport_preference"
    ],
    template=(
        "Welcome to the {city} travel guide for your {days}-day trip in {month}!\n"
        "Based on your preferences:\n"
        "- Interests: {interests}\n"
        "- Travel Pace: {travel_pace}\n"
        "- Traveling With: {travel_companions}\n"
        "- Preferred Transport: {transport_preference}\n\n"
        "1. Must-visit attractions.\n"
        "2. Local cuisine recommendations.\n"
        "3. Useful phrases in {language}.\n"
        "4. Budget tips to stay within {budget}.\n\n"
        "Enjoy your trip!"
    )
)

def get_trip_response_structured(params, max_retries=3):
    for attempt in range(max_retries):
        try:
            return (prompt_template | llm).invoke(params).content
        except TooManyRequestsError:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10
                time.sleep(wait_time)
            else:
                raise


def run_structured():
    st.markdown("<h2 style='text-align: center; color: #ffffff; font-size: 1.8rem; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>Guided Form Mode</h2>", unsafe_allow_html=True)
    
    # Show hint about enhanced cities
    cities_list = ', '.join(SUPPORTED_CITIES[:-1]) + ' and ' + SUPPORTED_CITIES[-1]
    st.info("📍 **You can enter ANY city** - AI will generate itinerary for all destinations!\n\n"
            f"💡 **Cities with weather & map support:** {cities_list}")
    
    # Initialize session state for storing generated itinerary
    if "structured_itinerary" not in st.session_state:
        st.session_state.structured_itinerary = None
        st.session_state.structured_city = None
        st.session_state.structured_month = None
        st.session_state.structured_is_supported = False

    city = st.text_input("City:", placeholder="e.g., Paris, Rome, Berlin")
    days = st.number_input("Days:", min_value=1, step=1)
    month = st.selectbox("Month:", options=[""] + MONTHS, index=0)
    language = st.text_input("Language:", placeholder="e.g., English, French")
    budget_amount = st.number_input("Budget (USD):", min_value=0, step=50)
    budget = f"${budget_amount}"

    interests = st.multiselect(
        "Interests:",
        [
            "Culture and history", "Food and drinks", "Nature and adventure",
            "Shopping", "Nightlife", "Art and museums", "Relaxation"
        ],
        default=["Culture and history"]
    )
    travel_pace = st.selectbox("Travel pace:", ["Relaxed", "Moderate", "Intense"])
    travel_companions = st.selectbox(
        "Traveling with:", ["Solo", "Partner", "Friends", "Family", "Group"]
    )
    transport_preference = st.selectbox(
        "Preferred transport:", ["Public", "Walking", "Taxi", "Rental car", "Bicycle"]
    )

    if st.button("Generate", key="gen_structured"):
        if not city or not month or not language:
            st.warning("Please fill in all required fields: City, Month, and Language.")
        else:
            if not COHERE_API_KEY:
                st.error("COHERE_API_KEY environment variable is not set. Please set it before running the app.")
            else:
                try:
                    params = {
                        "city": city,
                        "days": days,
                        "month": month,
                        "language": language,
                        "budget": budget,
                        "interests": ", ".join(interests),
                        "travel_pace": travel_pace,
                        "travel_companions": travel_companions,
                        "transport_preference": transport_preference
                    }
                    with st.spinner("Generating your travel itinerary..."):
                        itinerary = get_trip_response_structured(params)
                    st.session_state.structured_itinerary = itinerary
                    st.session_state.structured_city = city
                    st.session_state.structured_month = month
                    # Check if city is one of the supported cities
                    st.session_state.structured_is_supported = get_city_match(city) is not None
                except TooManyRequestsError:
                    st.error("⚠️ Rate limit exceeded. Please wait a few minutes and try again. Cohere API has rate limits to prevent overuse.")
                    st.info("💡 Tip: Try again in 1-2 minutes.")
                except Exception as e:
                    st.error(f"Error generating itinerary: {str(e)}")
                    st.exception(e)
    
    # Display stored itinerary, weather, and map
    if st.session_state.structured_itinerary:
        st.markdown("---")
        st.subheader("📋 Your Itinerary")
        st.markdown(st.session_state.structured_itinerary)
        
        # Only show weather and map for supported cities
        if st.session_state.structured_is_supported:
            matched_city = get_city_match(st.session_state.structured_city)
            
            # Display weather forecast
            if matched_city and st.session_state.structured_month:
                display_weather_card(matched_city, st.session_state.structured_month)
            
            # Display interactive map
            if matched_city:
                st.markdown("---")
                display_city_map(matched_city)
        else:
            st.markdown("---")
            st.info(f"ℹ️ **{st.session_state.structured_city}** is not in our enhanced database. "
                   f"Weather forecast and interactive map are available for: {', '.join(SUPPORTED_CITIES)}")

