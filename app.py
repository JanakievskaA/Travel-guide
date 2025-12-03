import streamlit as st
from app import run_structured, run_free_form

st.set_page_config(page_title="Smart Travel Guide", page_icon="🗺️")
st.title("🗺️ Smart Travel Guide")

tab_guided, tab_free = st.tabs(["📝 Guided Form", "💬 Free Text"])

with tab_guided:
    run_structured()

with tab_free:
    run_free_form()