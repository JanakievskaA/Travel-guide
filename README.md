
# Smart Travel Guide 

Smart Travel Guide is a modular, AI-driven trip planner designed to streamline the creation of personalized, day-by-day itineraries. Built on Streamlit and LangChain, this project demonstrates how guided forms and free-text inputs can feed into large language models and RAG pipelines to deliver context-rich travel recommendations.

## Architecture & Components

- **app.py**: Entry point defining two tabs: Guided Form and Free Text.
- **structured_mode.py**: Implements Guided Form Mode: users fill structured fields (city, days, budget, etc.). Uses a PromptTemplate to format inputs and invokes CohereChat for itinerary generation.
- **free_form_mode.py**: Implements Free Text Mode: natural-language user requests are parsed into itineraries. Integrates a RAG chain by calling `initialize_rag()` to load and query a local document store.
- **rag.py**: Configures ChromaDB embeddings and Cohere for vector storage. Builds a conversation-aware retrieval chain (`RunnableWithMessageHistory`) to support **Get More Details**.
- **rag.txt**: A plain-text corpus with local tips, museum facts, and hidden gems that enriches responses on demand.

## Key Technologies

- **Streamlit**: Rapid UI development with minimal code.
- **LangChain**: Chains of prompts, caching, and RAG orchestration.
- **Cohere**: LLM for generating conversational itineraries.
- **ChromaDB**: Fast, local vector store for embedding-based retrieval.
- **@st.cache_data / @st.cache_resource**: Efficient reuse of computed results and resources.

