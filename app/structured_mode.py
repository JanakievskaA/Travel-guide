import time
import streamlit as st
from cohere.errors import TooManyRequestsError
from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate
from config import COHERE_API_KEY, COHERE_MODEL

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

@st.cache_data
def get_trip_response_structured(params):
    try:
        return (prompt_template | llm).invoke(params).content
    except TooManyRequestsError:
        time.sleep(6)
        return (prompt_template | llm).invoke(params).content


def run_structured():
    st.header("Guided Form Mode")

    city = st.text_input("City:")
    days = st.number_input("Days:", min_value=1, step=1)
    month = st.text_input("Month:")
    language = st.text_input("Language:")
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
                    st.markdown(itinerary)
                except Exception as e:
                    st.error(f"Error generating itinerary: {str(e)}")
                    st.exception(e)

