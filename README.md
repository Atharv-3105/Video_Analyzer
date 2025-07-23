# 📽️ Agentic AI Video Analyzer 🔎

An intelligent video analysis tool powered by a sophisticated agentic AI. Upload any video and ask complex questions to get detailed, evidence-based insights.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agentic-video-analyzer.streamlit.app/)

---

## ✨ Features

* **Agentic AI Core**: Utilizes a multi-step reasoning process (Triage, Decomposition, Synthesis, Research, Formulation) to provide deep, accurate analysis.
* **Conversational Interface**: Chat with your video in a natural way. The agent can handle both analytical queries and casual conversation with a witty, charismatic persona.
* **Evidence-Based Responses**: All claims are grounded in specific visual or auditory evidence from the video, complete with timestamps for verification.
* **Multi-Modal Understanding**: Analyzes both visual elements (objects, text, scenes) and audio components (dialogue, tone, music) to build a complete picture.
* **Interactive UI**: A clean and intuitive web interface built with Streamlit, providing a seamless user experience.

---

## 🛠️ Tech Stack

* **Backend/AI**:
    * Python 3.x
    * Google Gemini (for advanced generative AI capabilities)
    * LangChain / Custom Agent Framework
* **Frontend**:
    * Streamlit

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* Python 3.8 or higher
* An API key for Google Gemini.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Atharv-3105/Video_Analyzer.git](https://github.com/Atharv-3105/Video_Analyzer.git)
    cd Video_Analyzer
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment variables:**
    * Create a file named `.env` in the root directory of the project.
    * Add your Google API key to this file:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

### Running the Application

Once the setup is complete, you can run the Streamlit app with the following command:

```bash
streamlit run app.py

---
### 💡 How It Works
#### The application's intelligence comes from a carefully engineered prompt in agents/video_agent.py. This prompt instructs the AI to follow a specific workflow:

* Intent Routing: First, it determines if the user is asking an analytical question or just having a conversation.

* Analysis Workflow: For analytical queries, it performs a deep, multi-modal analysis of the video.

* Response Formulation: It synthesizes its findings to construct a detailed, evidence-based answer that directly addresses the user's query.

* This structured approach ensures high-quality, reliable, and insightful responses every time.
