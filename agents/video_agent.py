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
def analyze_video(agent, video_path, user_query):
    uploaded_video = upload_file(video_path)
    while uploaded_video.state.name == "Processing":
        time.sleep(1)
        uploaded_video = get_file(uploaded_video.name)
    
    prompt= (
        f'''
            You are a video content and context analyzer.

            Your job is to:
            1. Analyze the uploaded video thoroughly.
            2. Understand the video’s content, tone, setting, and any implicit or explicit context.
            3. Use supplementary web research if needed to enhance accuracy and depth.

            Then, respond to the following user query using insights from the video and any relevant external data:

            {user_query}

            Your response must be:
            - Detailed and accurate
            - Easy for anyone to understand
            - Actionable and practical
            - Delivered with a witty and humorous tone (keep it friendly, not sarcastic)

            Think of yourself as the Sherlock Holmes of video, but funnier and with internet access.

        '''
    )
    
    result = agent.run(prompt, videos = [uploaded_video])
    return result.content