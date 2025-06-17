# Smart Travel Guide 🌍

Smart Travel Guide is an AI-powered trip planning application built with **Streamlit** and **LangChain**. It provides two intuitive modes for generating personalized day-by-day itineraries based on user preferences and free-text descriptions. Additionally, it integrates a Retrieval-Augmented Generation (RAG) chain to fetch supplementary details from a local `rag.txt` document.

## 🚀 Features

- **Guided Form Mode**: Structured input for city, duration, month, language, budget, interests, travel pace, companions, and transport preference.
- **Free Text Mode**: Describe your trip in plain language (e.g., “I’m traveling to Rome solo for 3 days with a $400 budget”) and receive a detailed itinerary.
- **RAG Integration**: Leverages ChromaDB embeddings and Cohere to index `rag.txt` and supply on-demand context when clicking **Get More Details**.
- **Caching**:
  - `@st.cache_data` for LLM responses to reduce redundant API calls.
  - `@st.cache_resource` for persistent vector store initialization.
