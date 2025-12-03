import os
import time
import streamlit as st
from cohere.errors import TooManyRequestsError
from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate
from rag import initialize_rag

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
llm = ChatCohere(model="command-r-plus-08-2024", cohere_api_key=COHERE_API_KEY)

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

@st.cache_data
def get_trip_response_free(raw_text):
    try:
        return (travel_prompt | llm).invoke({"raw_request": raw_text}).content
    except TooManyRequestsError:
        time.sleep(6)
        return (travel_prompt | llm).invoke({"raw_request": raw_text}).content


def run_free_form():
    st.header("Free Text Mode")

    if "free_history" not in st.session_state:
        st.session_state.free_history = []

    chain_with_history, retriever, error = initialize_rag()
    if error:
        st.error(error)
        return

    raw_request = st.text_input("Describe your trip…", key="free_raw")

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
                    st.session_state.free_history.insert(0, {
                        "request": raw_request,
                        "response": itinerary,
                        "rag_details": None
                    })
                except Exception as e:
                    st.error(f"Error generating itinerary: {str(e)}")
                    st.exception(e)

    for i, entry in enumerate(st.session_state.free_history):
        st.markdown(f"**You:** {entry['request']}")
        st.markdown(f"**Itinerary:** {entry['response']}")

        if st.button("Get More Details", key=f"rag_details_{i}"):
            try:
                response = chain_with_history.invoke(
                    {"input": f"Provide detailed information about the attractions: {entry['request']}"},
                    config={"configurable": {"session_id": "free_session"}}
                )
                st.session_state.free_history[i]["rag_details"] = response["answer"]
            except TooManyRequestsError:
                time.sleep(6)
                response = chain_with_history.invoke(
                    {"input": f"Provide detailed information about the attractions: {entry['request']}"},
                    config={"configurable": {"session_id": "free_session"}}
                )
                st.session_state.free_history[i]["rag_details"] = response["answer"]
            except Exception as e:
                st.error(f"Error fetching details: {e}")

        if entry.get("rag_details"):
            st.markdown(f"**More Details:** {entry['rag_details']}")

        st.markdown("---")

