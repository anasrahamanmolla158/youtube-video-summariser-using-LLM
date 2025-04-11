import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re  # For handling various YouTube URL formats

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt template for generating a summary

prompt = """You are a YouTube video summarizer. You will take the transcript text 
and summarize the entire video, providing the key points in details
also format the final out with emoji and icon for each heading and imprtant text also
and write heading with h1 and subheading with h3 and also bold importent words in the body points . 
Here is the transcript text: """

# Function to extract the YouTube video ID from various types of URLs
def extract_video_id(url):
    # Regular expression to capture the video ID from standard, shortened, or embed URLs
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# Fetch transcript data from YouTube
def extract_transcript_details(video_id):
    try:
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        return f"Error: {str(e)}"

# Generate summary using Gemini API
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app setup
# Function to check if the link is from YouTube or Facebook
def check_video_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "facebook.com" in url:
        return "facebook"
    else:
        return "unsupported"

st.title("📽 Get Youtube summary")
video_link = st.text_input("Enter Video Link:")

if video_link:
    platform = check_video_platform(video_link)
    
    if platform == "youtube":
        video_id = extract_video_id(video_link)
        if video_id:
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        else:
            st.error("Invalid YouTube link. Please provide a valid YouTube video URL.")
    
    elif platform == "facebook":
        st.error("Facebook videos are not supported for transcript retrieval at this time.")
    
    else:
        st.error("Unsupported video platform. Please provide a valid YouTube link .")

if st.button(" ✨ Get Detailed Notes "):
    if platform == "youtube":
        if video_id:
            with st.spinner('Retrieving transcript and generating summary...'):
                transcript_text = extract_transcript_details(video_id)
                
                if "Error" in transcript_text:
                    st.error(transcript_text)
                else:
                    summary = generate_gemini_content(transcript_text, prompt)
                    if "Error" in summary:
                        st.error(summary)
                    else:
                        st.markdown("## 📝 Detailed Notes:")
                        st.write(summary)
        else:
            st.error("Please enter a valid YouTube video link.")
    
    elif platform == "facebook":
        st.error("Facebook videos are not supported for transcript retrieval.")
