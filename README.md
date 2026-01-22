# Smart Travel Guide

Smart Travel Guide is a modern, AI-driven trip planner designed to streamline the creation of personalized, day-by-day itineraries with interactive maps and weather insights. Built on Streamlit and LangChain, this project demonstrates how guided forms and free-text inputs can feed into large language models and RAG pipelines to deliver context-rich travel recommendations. Works with any city worldwide, with enhanced features (maps, weather, detailed info) available for 10 major European destinations.

## Architecture & Components

- **app.py**: Entry point with modern UI featuring hero section, feature cards, and two tabs: Guided Form and Free Text
- **app/structured_mode.py**: Implements Guided Form Mode: users fill structured fields (city, days, budget, etc.) with modern input styling. Uses a PromptTemplate to format inputs and invokes CohereChat for itinerary generation. Includes "Get More Details" RAG functionality for supported European cities
- **app/free_form_mode.py**: Implements Free Text Mode: natural-language user requests are parsed into itineraries. Integrates conditional RAG chain for supported cities only via "Get More Details" button
- **app/map_utils.py**: Provides interactive Folium maps with attraction markers and city-specific data loading
- **app/weather_utils.py**: Delivers monthly weather forecasts, packing recommendations, and activity suggestions based on temperature and conditions
- **app/rag.py**: Configures ChromaDB embeddings and Cohere for vector storage. Builds a conversation-aware retrieval chain (`RunnableWithMessageHistory`) for detailed information on supported cities
- **data/rag.txt**: Comprehensive plain-text corpus with local tips, museum facts, hidden gems, and insider information for 10 European cities
- **data/cities.json**: Structured data containing coordinates, attractions, and categories for all supported cities
- **config.py**: Centralized configuration for API keys, models, data paths, and supported cities list


## Enhanced Features

Available in both Guided Form and Free Text modes:

- **Interactive Maps**: Folium-based maps with categorized attraction markers
- **Weather Forecasts**: Monthly weather data with packing and activity recommendations
- **Detailed Information**: RAG-powered "Get More Details" button for insider tips and local knowledge

## Key Technologies

- **Streamlit**: Modern UI development with custom CSS styling
- **LangChain**: Chains of prompts, caching, and RAG orchestration
- **Cohere**: LLM for generating conversational itineraries (command-r-plus-08-2024)
- **ChromaDB**: Fast, local vector store for embedding-based retrieval
- **Folium**: Interactive mapping library for geographical visualizations
- **@st.cache_resource**: Efficient reuse of computed results and resources
