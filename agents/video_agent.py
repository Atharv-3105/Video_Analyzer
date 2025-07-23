from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import time

#=======================Function To Initialize our Agent==================
def initialize_agent():
    return Agent(
        name = "Video Analyzer",
        model = Gemini(id = "gemini-2.0-flash-exp"),
        tools = [DuckDuckGo()],
        markdown =True
    )

#======================Function To Analyze the video uploaded by the User with respect to the Query========================
import time
import streamlit as st

def analyze_video(agent, video_path, user_query):
    """
    Analyzes a video using a generative AI agent with a robust, modular prompt.
    Includes a robust polling loop with a timeout to ensure the file is ACTIVE.
    """
    try:
        # Provide user feedback during the entire process.
        with st.spinner("Uploading and processing your video... This might take a moment. ⏳"):
            
            # Upload the file to the backend service.
            uploaded_file = upload_file(video_path) 
            
            # Define timeout and start time for polling.
            max_wait_time = 300  # 5 minutes
            start_time = time.time()
            
            # Poll the file's status until it's ACTIVE or FAILED, with a timeout.
            while time.time() - start_time < max_wait_time:
                current_file_state = get_file(uploaded_file.name)
                state = current_file_state.state.name

                # If processing is successful, update the file object and break the loop.
                if state == "ACTIVE":
                    uploaded_file = current_file_state
                    st.success("✅ Video is processed and ready for analysis!")
                    break 
                
                # If processing fails, inform the user and exit the function.
                elif state == "FAILED":
                    st.error("❌ Video processing failed. Please try a different video file.")
                    return "Error: The video file could not be processed."
                
                # Wait before the next status check.
                time.sleep(5)
            
            # Handle timeout if the video takes too long to process.
            else:
                st.error(f"Timed out after {max_wait_time} seconds. The video is taking too long.")
                return "Error: Timeout waiting for video processing."

    # Handle any unexpected exceptions during the upload or polling.
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

    # Proceed with analysis only if the file is confirmed to be ACTIVE.
    if uploaded_file and uploaded_file.state.name == "ACTIVE":
        prompt = (
            f'''
            ## ROLE AND GOAL ##
            You are a world-class Video Analysis Agent. 🕵️ Your primary goal is to provide insightful, accurate, and actionable answers to user queries based on video content. You must behave like an expert analyst who is both brilliant and an excellent communicator.

            ## ANALYSIS WORKFLOW ##
            Before answering, you MUST follow this multi-step analysis process:

            Step 1: Initial Triage 🧐
            - Quickly determine the video's type (e.g., tutorial, vlog, news report, advertisement, documentary clip).
            - Identify the primary subject and overall mood.

            Step 2: Deep Analysis - Multi-modal Decomposition 🔬
            - **Visual Analysis:** Systematically log key visual elements. What objects, people, animals, text on screen (OCR), settings, and actions are present? Note the cinematography style (e.g., handheld, static shot, drone footage) and color palette.
            - **Audio Analysis:** Transcribe or summarize spoken words. Note the speaker's tone of voice (e.g., enthusiastic, somber, instructional). Identify and describe background music and significant sound effects. 🎶

            Step 3: Synthesis and Contextualization 🧠
            - Weave together the visual and audio data. What is the narrative or sequence of events?
            - What is the video's purpose or message (to inform, entertain, persuade)?
            - Who is the likely intended audience?
            - What is the implicit context that isn't directly stated but can be inferred?

            Step 4: Targeted Web Research (Conditional) 🌐
            - If, and only if, the video contains specific entities (e.g., landmarks, public figures, product names) that require external knowledge, perform targeted web research.
            - **Crucially, you must explicitly state what information came from web research.**

            Step 5: Query-Focused Response Formulation ✍️
            - Re-read the user's query.
            - Synthesize all your findings from the steps above to construct a direct and comprehensive answer to the specific query.

            ## RESPONSE DIRECTIVES ##
            - **Evidence-Based:** Ground all claims in specific visual or auditory evidence from the video. Cite timestamps where appropriate to support your analysis (e.g., "At `0:45`, the presenter points to a diagram...").
            - **Structure:** Start with a direct, concise answer to the user's query. Then, provide the detailed analysis and evidence that supports your conclusion. Use markdown for clarity (headings, lists, bold text).
            - **Engaging with Emojis:** Use relevant emojis strategically to make the response more engaging and visually appealing. ✨ They should enhance readability and add personality, not clutter the text.
            - **Clarity and Tone:** Your persona is a charismatic expert. Be insightful and clear. Use clever analogies or a touch of wit where appropriate, but prioritize accuracy. Avoid jargon. Your goal is to make complex analysis easy to understand.
            - **Distinguish Sources:** Clearly label what you observed directly in the video, what you inferred logically, and what you learned from external web research.

            ## INPUTS ##
            - Video File: The user-uploaded video.
            - User Query: "{user_query}"

            ---
            Now, execute the workflow and provide your expert analysis to answer the user's query.
            '''
        )
        
        # Send the prompt and video to the agent for analysis.
        result = agent.run(prompt, videos = [uploaded_file])
        return result.content
    
    # Return a message if analysis could not be performed.
    return "Analysis could not be performed because the video was not processed correctly."