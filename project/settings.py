import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()
deepseek_key = st.secrets["api_keys"]["DEEPSEEK_API_KEY"]
# API Keys
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", deepseek_key)

# Model Settings
DEFAULT_MODEL = "openrouter/deepseek/deepseek-r1:free"
API_BASE_URL = "https://openrouter.ai/api/v1"

# Verify configuration on startup
def verify_config():
    """Verify that required configuration is present."""
    missing_keys = []
    
    if not DEEPSEEK_API_KEY:
        missing_keys.append("DEEPSEEK_API_KEY")
    
    if missing_keys:
        print(f"Warning: Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set these in your .env file.")
        return False
    
    return True