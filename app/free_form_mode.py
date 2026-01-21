import time
import re
import streamlit as st
from cohere.errors import TooManyRequestsError
from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate
from .rag import initialize_rag
from .map_utils import display_city_map, get_city_match
from .weather_utils import display_weather_card
from config import COHERE_API_KEY, COHERE_MODEL, SUPPORTED_CITIES

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def get_month_match(user_input: str) -> str | None:
    """Find matching month from user input."""
    user_input_lower = user_input.lower()
    for month in MONTHS:
        if month.lower() in user_input_lower:
            return month
    return None

llm = ChatCohere(model=COHERE_MODEL, cohere_api_key=COHERE_API_KEY)

travel_prompt = PromptTemplate(
    input_variables=["raw_request"],
    template=(
        "You are an expert travel assistant. A user says: \"{raw_request}\".\n"
        "Extract details (city, duration, month, budget, interests) from that sentence \n"
        "and generate a clear day-by-day itinerary including:\n"
        "- Top attractions\n"
        "- Local food tips with approximate costs\n"
        "- Useful local phrases\n"
        "- Budget breakdown staying within their budget.\n\n"
        "If you don't know which city that is, say you've never heard of it.\n"
        "Enjoy your trip!"
    )
)

def get_trip_response_free(raw_text, max_retries=3):
    for attempt in range(max_retries):
        try:
            return (travel_prompt | llm).invoke({"raw_request": raw_text}).content
        except TooManyRequestsError:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10
                time.sleep(wait_time)
            else:
                raise


def run_free_form():
    st.markdown("<h2 style='text-align: center; color: #ffffff; font-size: 1.8rem; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>Free Text Mode</h2>", unsafe_allow_html=True)
    
    cities_list = ', '.join(SUPPORTED_CITIES[:-1]) + ' and ' + SUPPORTED_CITIES[-1]
    st.info("📍 **You can enter ANY city** - AI will generate itinerary for all destinations!\n\n"
            f"💡 **Cities with weather & map support:** {cities_list}")

    if "free_history" not in st.session_state:
        st.session_state.free_history = []

    # Check if we have any supported cities in history that might need RAG
    has_supported_cities = any(
        get_city_match(entry.get("city")) is not None
        for entry in st.session_state.free_history
    )

    # Only initialize RAG if we have supported cities or if user just generated something
    chain_with_history, retriever, error = None, None, None
    if has_supported_cities:
        chain_with_history, retriever, error = initialize_rag()
        if error:
            st.warning("RAG system temporarily unavailable, but you can still generate itineraries.")

    raw_request = st.text_area("Describe your trip", key="free_raw", height=100, 
                                placeholder="Example: I want to visit Paris for 5 days in June with a budget of $2000. I love art and good food.")

    if st.button("Generate", key="gen_free"):
        if not raw_request.strip():
            st.warning("Please enter your travel request.")
        else:
            if not COHERE_API_KEY:
                st.error("COHERE_API_KEY environment variable is not set. Please set it before running the app.")
            else:
                try:
                    with st.spinner("Generating your travel itinerary..."):
                        itinerary = get_trip_response_free(raw_request)
                    
                    # Try to detect city and month from request
                    detected_city = get_city_match(raw_request)
                    detected_month = get_month_match(raw_request)
                    
                    st.session_state.free_history.insert(0, {
                        "request": raw_request,
                        "response": itinerary,
                        "rag_details": None,
                        "city": detected_city,
                        "month": detected_month
                    })
                except TooManyRequestsError:
                    st.error("⚠️ Rate limit exceeded. Please wait a few minutes and try again. Cohere API has rate limits to prevent overuse.")
                    st.info("💡 Tip: Try again in 1-2 minutes, or use the Guided Form mode which may have better caching.")
                except Exception as e:
                    st.error(f"Error generating itinerary: {str(e)}")
                    st.exception(e)

    for i, entry in enumerate(st.session_state.free_history):
        st.markdown(f"**You:** {entry['request']}")
        st.markdown(f"**Itinerary:** {entry['response']}")
        
        # Only show weather and map for supported cities
        if entry.get("city"):
            # Check if city is supported
            is_supported = get_city_match(entry["city"]) is not None

            if is_supported:
                # Display weather if city and month were detected
                if entry.get("month"):
                    display_weather_card(entry["city"], entry["month"])

                # Display map
                display_city_map(entry["city"])

                # Show Get More Details button for supported cities
                if st.button("Get More Details", key=f"rag_details_{i}"):
                    try:
                        # Initialize RAG only when needed
                        if chain_with_history is None:
                            chain_with_history, retriever, error = initialize_rag()
                            if error:
                                st.error("Unable to load detailed information at this time.")
                                return

                        response = chain_with_history.invoke(
                            {"input": f"Provide detailed information about the attractions: {entry['request']}"},
                            config={"configurable": {"session_id": "free_session"}}
                        )
                        st.session_state.free_history[i]["rag_details"] = response["answer"]
                    except TooManyRequestsError:
                        st.error("⚠️ Rate limit exceeded. Please wait a few minutes before requesting more details.")
                    except Exception as e:
                        st.error(f"Error fetching details: {e}")
            else:
                # City not in supported list - show info message
                cities_list = ', '.join(SUPPORTED_CITIES[:-1]) + ' and ' + SUPPORTED_CITIES[-1]
                st.info(f"ℹ️ Weather forecast and interactive map are available for: {cities_list}")
        else:
            # No city detected - show general info
            cities_list = ', '.join(SUPPORTED_CITIES[:-1]) + ' and ' + SUPPORTED_CITIES[-1]
            st.info(f"ℹ️ Weather forecast and interactive map are available for: {cities_list}")

        if entry.get("rag_details"):
            st.markdown(f"**More Details:** {entry['rag_details']}")

        st.markdown("---")

