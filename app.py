import streamlit as st
from app import run_structured, run_free_form

st.set_page_config(
    page_title="Smart Travel Guide",
    page_icon="🗺️",
    layout="wide"
)

# Modern CSS styling
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
    /* Hero section with gradient background */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    /* Hero title */
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 0;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 0.8rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #f0f0f0;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
    }
    
    .feature-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #2d3436;
        margin: 0.3rem 0;
    }
    
    .feature-desc {
        font-size: 0.8rem;
        color: #636e72;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 60px;
        background: #f8f9fa;
        padding: 20px 40px;
        border-radius: 16px;
        justify-content: center;
        border: 2px solid #e9ecef;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1.3rem;
        font-weight: 600;
        padding: 18px 45px;
        border-radius: 12px;
        color: #000000 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e9ecef;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Buttons */
    .stButton > button {
        font-size: 1.1rem;
        font-weight: 600;
        padding: 12px 28px;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd6 0%, #6a4190 100%) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        background: #4a5568 !important;
        transform: translateY(0);
    }
    
    /* Inputs - Gray background */
    .stTextInput input, .stTextArea textarea {
        font-size: 1.1rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.2);
        background: rgba(60, 60, 70, 0.8);
        color: #ffffff;
        padding: 12px 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .stSelectbox > div > div {
        font-size: 1.1rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.2);
        background: rgba(60, 60, 70, 0.8);
        color: #ffffff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .stNumberInput input {
        font-size: 1.1rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.2);
        background: rgba(60, 60, 70, 0.8);
        color: #ffffff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .stMultiSelect > div {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.2);
        background: rgba(60, 60, 70, 0.8);
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* MultiSelect selected items - Violet color */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] span {
        color: white !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] svg {
        fill: white !important;
    }
    
    /* Labels - White color */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label, .stMultiSelect label {
        font-size: 1.15rem;
        font-weight: 600;
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Placeholder text */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: rgba(255,255,255,0.5);
        font-style: italic;
    }
    
    /* Number input - hide +/- buttons completely */
    .stNumberInput button {
        display: none !important;
    }
    
    /* Number input - remove red focus */
    .stNumberInput input {
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    .stNumberInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
        outline: none !important;
    }
    
    .stNumberInput > div {
        border: none !important;
        box-shadow: none !important;
    }
    
    .stNumberInput [data-baseweb="base-input"] {
        border-color: #667eea !important;
    }
    
    .stNumberInput [data-baseweb="base-input"]:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Focus states - Violet */
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3) !important;
        outline: none !important;
    }
    
    /* Number input focus */
    .stNumberInput div[data-baseweb="input"]:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Override any red focus states */
    *:focus {
        outline-color: #667eea !important;
    }
    
    input:focus, textarea:focus, select:focus, button:focus {
        outline: none !important;
        border-color: #667eea !important;
    }
    
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"]:focus-within,
    div[data-baseweb="base-input"]:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Selectbox hover */
    .stSelectbox > div > div:hover {
        border-color: #667eea !important;
    }
    
    /* General link and accent colors */
    a, .st-emotion-cache-1gulkj5 {
        color: #667eea !important;
    }
    
    /* Override any red colors */
    .st-emotion-cache-1inwz65, .st-emotion-cache-nahz7x {
        background-color: #667eea !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
    }
    
    h2 {
        font-size: 1.6rem;
        color: #2d3436;
        border-bottom: 3px solid #667eea;
        padding-bottom: 8px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #ffffff;
        border-top: 1px solid rgba(255,255,255,0.2);
        margin-top: 3rem;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">Smart Travel Guide</div>
    <div class="hero-subtitle">Plan your perfect adventure with AI-powered itineraries</div>
</div>
""", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI-Powered</div>
        <div class="feature-desc">Smart itinerary generation</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌤️</div>
        <div class="feature-title">Weather Insights</div>
        <div class="feature-desc">Pack right for your trip</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🗺️</div>
        <div class="feature-title">Interactive Maps</div>
        <div class="feature-desc">Explore destinations visually</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Tabs
tab_guided, tab_free = st.tabs(["📝 Guided Form", "💬 Free Text"])

with tab_guided:
    run_structured()

with tab_free:
    run_free_form()

