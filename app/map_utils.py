import json
import folium
from streamlit_folium import folium_static
import streamlit as st
from config import CITIES_DATA_FILE, SUPPORTED_CITIES


def load_cities_data():
    """Load cities data from JSON file."""
    try:
        with open(CITIES_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_city_match(user_input: str) -> str | None:
    """Find matching city from supported cities list."""
    user_input_lower = user_input.lower()
    for city in SUPPORTED_CITIES:
        if city.lower() in user_input_lower:
            return city
    return None


def create_city_map(city_name: str) -> folium.Map | None:
    """Create a folium map for a given city with attraction markers."""
    cities_data = load_cities_data()
    
    if city_name not in cities_data:
        return None
    
    city_info = cities_data[city_name]
    center = city_info["center"]
    zoom = city_info["zoom"]
    attractions = city_info["attractions"]
    
    # Create base map with a nice tile style
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="CartoDB positron"
    )
    
    # Color mapping for categories
    category_colors = {
        "landmark": "#e74c3c",      # Red
        "museum": "#9b59b6",         # Purple
        "food": "#f39c12",           # Orange
        "nature": "#27ae60",         # Green
        "shopping": "#3498db",       # Blue
        "activity": "#1abc9c",       # Teal
        "neighborhood": "#95a5a6",   # Gray
        "entertainment": "#e91e63"   # Pink
    }
    
    # Category icons (Font Awesome)
    category_icons = {
        "landmark": "monument",
        "museum": "university",
        "food": "utensils",
        "nature": "leaf",
        "shopping": "shopping-bag",
        "activity": "star",
        "neighborhood": "home",
        "entertainment": "gamepad"
    }
    
    # Add markers for each attraction
    for attraction in attractions:
        name = attraction["name"]
        coords = attraction["coords"]
        category = attraction.get("category", "landmark")
        
        color = category_colors.get(category, "#3498db")
        icon = category_icons.get(category, "info-sign")
        
        # Create popup with attraction name
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 150px;">
            <h4 style="margin: 0 0 5px 0; color: {color};">{name}</h4>
            <p style="margin: 0; color: #666; font-size: 12px;">
                📍 {category.title()}
            </p>
        </div>
        """
        
        folium.Marker(
            location=coords,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=name,
            icon=folium.Icon(color=color.replace("#", ""), icon=icon, prefix='fa')
        ).add_to(m)
    
    # Add a legend
    legend_html = """
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; 
                background-color: white; padding: 10px; border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2); font-family: Arial;">
        <h4 style="margin: 0 0 8px 0;">Legend</h4>
        <div style="display: flex; flex-direction: column; gap: 4px; font-size: 12px;">
            <span>🔴 Landmarks</span>
            <span>🟣 Museums</span>
            <span>🟠 Food & Dining</span>
            <span>🟢 Nature</span>
            <span>🔵 Shopping</span>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m


def display_city_map(city_name: str):
    """Display an interactive map for the specified city in Streamlit."""
    city_map = create_city_map(city_name)
    
    if city_map:
        st.markdown("---")
        st.subheader(f"Interactive Map: {city_name}")
        st.caption("Click on markers to see attraction details")
        folium_static(city_map, width=700, height=500)
        
        # Show attractions list
        cities_data = load_cities_data()
        if city_name in cities_data:
            attractions = cities_data[city_name]["attractions"]
            
            with st.expander("Attractions in this city", expanded=False):
                for i, attr in enumerate(attractions, 1):
                    category_emoji = {
                        "landmark": "🏛️",
                        "museum": "🎨",
                        "food": "🍽️",
                        "nature": "🌳",
                        "shopping": "🛍️",
                        "activity": "⭐",
                        "neighborhood": "🏘️",
                        "entertainment": "🎢"
                    }
                    emoji = category_emoji.get(attr.get("category", "landmark"), "📍")
                    st.write(f"{i}. {emoji} **{attr['name']}**")
    else:
        st.info(f"Map not available for {city_name}. Supported cities: {', '.join(SUPPORTED_CITIES)}")

