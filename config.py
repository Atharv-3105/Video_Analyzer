import os
from dotenv import load_dotenv
import streamlit as st 
import google.generativeai as genai

def configure_env():
    api_key = None
    
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        print(f"API_KEY Loaded from Streamlit.Secrets")
        
    except KeyError:
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            print("API_KEY Loaded from .env file")
        else:
            raise ValueError("Missing GOOGLE_API_KEY. Please set it in local_env or Streamlit.Secrets")
    if api_key:
        genai.configure(api_key = api_key)  
    else:
        raise ValueError("Failed to Load API_Key")
    
