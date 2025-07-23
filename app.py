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
st.title("📽️ Agentic_AI Video Analyzer 🔎")
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
                
#================Footer================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-style: italic; color: grey;">
        "What a privilege it is to be exhausted by a challenge you chose for yourself."
    </div>
    <br>
    <div style="text-align: center;">
        <p>
        Find me Here!: 
        <a href="https://github.com/Atharv-3105" target="_blank" style="text-decoration: none; color: inherit;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle; margin-right: 5px;"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>GitHub
        </a> | 
        <a href="https://www.linkedin.com/in/atharv3105/" target="_blank" style="text-decoration: none; color: inherit;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle; margin-right: 5px;"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>LinkedIn
        </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
        
           


