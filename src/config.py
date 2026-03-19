import os

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

def get_secret(key_name, default_value):
    """
    Intelligently fetch secrets for Streamlit Community Cloud deployment.
    Prioritizes st.secrets, then os.getenv, then defaults.
    """
    if HAS_STREAMLIT:
        try:
            return st.secrets[key_name]
        except (KeyError, FileNotFoundError, AttributeError):
            pass
    return os.getenv(key_name, default_value)

# API Keys
CRIC_API_KEY = get_secret("CRIC_API_KEY", "a6177fed-ecff-44e0-8e3a-2c1af4efad0c")
WEATHER_API_KEY = get_secret("WEATHER_API_KEY", "dummy_weather_api_key")

# Database configuration
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'predictor.db')
DB_PATH = os.path.abspath(DB_PATH)

# Models and data paths
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(DB_PATH), 'processed')
RAW_DATA_DIR = os.path.join(os.path.dirname(DB_PATH), 'raw')
