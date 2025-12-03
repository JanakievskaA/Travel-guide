"""
RAG (Retrieval-Augmented Generation) module for travel guide.
"""
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from config import COHERE_API_KEY, COHERE_MODEL, COHERE_EMBEDDING_MODEL, RAG_DATA_FILE, RAG_DB_DIR

embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY, model=COHERE_EMBEDDING_MODEL)
llm = ChatCohere(model=COHERE_MODEL, cohere_api_key=COHERE_API_KEY)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a travel expert. Use the provided context to create a detailed day-by-day travel itinerary.\n"
        "Include:\n"
        "- Top attractions\n"
        "- Local food recommendations with approximate costs\n"
        "- Useful phrases in the local language\n"
        "- Budget breakdown based on the user's budget\n"
        "If details are missing, politely request clarification.\n"
        "Context:\n{context}"
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

@st.cache_resource
def get_vector_store():
    try:
        docs = TextLoader(str(RAG_DATA_FILE)).load()
    except FileNotFoundError:
        return None, f"RAG data file not found at {RAG_DATA_FILE}."
    except Exception as e:
        return None, str(e)

    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
    store = Chroma.from_documents(chunks, embeddings, persist_directory=str(RAG_DB_DIR))
    return store, None

history_store = StreamlitChatMessageHistory(key="rag_history")

def initialize_rag():
    """
    Initialize RAG chain for conversational travel guide.
    
    Returns:
      chain: RunnableWithMessageHistory for conversational RAG
      retriever: VectorStore retriever
      error: Error message if loading failed
    """
    store, error = get_vector_store()
    if error:
        return None, None, error

    retriever = store.as_retriever()

    qa_chain = create_stuff_documents_chain(llm, prompt_template)

    retriever_chain = create_retrieval_chain(retriever, qa_chain)

    chain = RunnableWithMessageHistory(
        retriever_chain,
        lambda session_id: history_store,
        input_messages_key="input",
        history_messages_key="chat_history"
    )
    return chain, retriever, None

