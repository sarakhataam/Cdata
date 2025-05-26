import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    """Initialize and return the LLM instance"""
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-8b-latest",
        google_api_key=st.session_state.google_api_key,
        temperature=0.3
    )
google_key = st.secrets["api_keys"]["GOOGLE_API_KEY"]
def initialize_session_state():
    """Initialize all session state variables"""
    if 'google_api_key' not in st.session_state:
        st.session_state.google_api_key = os.getenv('GOOGLE_API_KEY', google_key)
        
    if 'df' not in st.session_state:
        st.session_state.df = None
        
    if 'original_df' not in st.session_state:
        st.session_state.original_df = None
    
    if 'df2' not in st.session_state:
        st.session_state.df2 = None
        
    if 'original_df2' not in st.session_state:
        st.session_state.original_df2 = None
        
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'figs' not in st.session_state:
        st.session_state.figs = []
        
    if 'crew_analysis_done' not in st.session_state:
        st.session_state.crew_analysis_done = False
        
    if 'questions' not in st.session_state:
        st.session_state.questions = []
        
    if 'viz_code' not in st.session_state:
        st.session_state.viz_code = None

    if 'generate_eda' not in st.session_state:
        st.session_state.generate_eda = False

    if 'profile' not in st.session_state:
        st.session_state.profile = None

    if "column_descriptions" not in st.session_state:
        st.session_state.column_descriptions = {}

    if "test_sample" not in st.session_state:
        st.session_state.test_sample = {}
    
    if "model" not in st.session_state:
        st.session_state.model = None
    
    if "matrics" not in st.session_state:
        st.session_state.matrics = None

    

def render_data_metrics(df):
    """Render data metrics in a row"""
    metrics_row = st.container()
    with metrics_row:
        cols = st.columns(4)
        with cols[0]:
            st.metric("Total Rows", f"{df.shape[0]:,}")
        with cols[1]:
            st.metric("Total Columns", df.shape[1])
        with cols[2]:
            num_cols = len(df.select_dtypes(include='number').columns)
            st.metric("Numeric Columns", num_cols)
        with cols[3]:
            cat_cols = len(df.select_dtypes(include=['object', 'category']).columns)
            st.metric("Categorical Columns", cat_cols)