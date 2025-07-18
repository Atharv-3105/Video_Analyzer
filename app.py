import streamlit as st 
from agents.video_agent import initialize_agent, analyze_video
from utils.file_utils import save_temp_file
from config import configure_env

from pathlib import Path
import os

#Load Environment Variables
configure_env()

#====================Web Page Design====================
st.set_page_config(page_title="AI Video Analyzer", page_icon="📽️", layout="wide")
st.title("📽️ AI Video Analyzer 🔎")
st.caption("Built with GEMINI 2.0 & PHI AGENT")

#====================Side-Bar Design====================
st.sidebar.header("Upload Video")
video_files = st.sidebar.file_uploader("Upload a Video", type=["mp4", "avi"])

#A success message for successfull upload of video
video_path = None
if video_files:
    video_path = save_temp_file(video_files)
    st.sidebar.video(video_path)
    st.sidebar.success("Video Uploaded Successfully ✅")
    
# Session state for chat_history and file_path

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]
    
if "agent" not in st.session_state:
    st.session_state.agent = initialize_agent()
    
#Main Code

if video_files and video_path:
    st.subheader("Chat with the video 💬")
    
    #Get the user input
    user_query = st.chat_input("Ask something about the video 💬")
    
    if user_query:
        st.session_state.chat_history.append({"role":"user", "content":user_query})
        
        #Call the agent for analyzing the video
        with st.spinner("Analyzing Video⌛"):
            try:
                response = analyze_video(agent=st.session_state.agent, video_path=video_path, user_query=user_query)
                st.session_state.chat_history.append({"role":"analyst", "content":response})
            except Exception as e:
                error_msg = f"Error: {e}"
                st.session_state.chat_history.append({"role":"analyst", "content":error_msg})
                
    #Output full conversation
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg['content'])
            
    #Add a Reset button to clear all the chat_history
    if st.sidebar.button("Clear Chat🗑️"):
        st.session_state.chat_history = []
        if video_path:
            ## It will safely delete the file at video_path if it exists; does nothing if it's already missing
            Path(video_path).unlink(missing_ok=True)
        st.rerun()
        
else:
    st.info("Upload a video for analysis:")
                
            
           


