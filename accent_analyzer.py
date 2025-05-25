import streamlit as st
import moviepy.editor as mp
import whisper
import speechbrain.pretrained as sb
import os
import requests
import tempfile
import subprocess
import torchaudio
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re

# Function to check ffmpeg installation
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        st.error("ffmpeg is not installed or not found in PATH. Please install ffmpeg and add it to your system PATH.")
        return False

# Function to convert Google Drive shared link to direct download URL
def get_google_drive_download_url(shared_url):
    match = re.search(r'file/d/([a-zA-Z0-9_-]+)', shared_url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    else:
        st.error("Invalid Google Drive URL. Use a shared link like 'https://drive.google.com/file/d/.../view'.")
        return None

# Function to download video
def download_video(video_url, output_path="temp_video.mp4"):
    try:
        # Handle Google Drive shared links
        if "drive.google.com" in video_url.lower():
            direct_url = get_google_drive_download_url(video_url)
            if not direct_url:
                return None
        else:
            direct_url = video_url

        # Set up requests with retry logic and User-Agent
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[403, 429, 500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = session.get(direct_url, stream=True, headers=headers, timeout=120)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return output_path
        else:
            st.error(f"Download failed: HTTP {response.status_code}. Ensure the URL is a direct MP4 or public Google Drive link ('Anyone with the link').")
            return None
    except Exception as e:
        st.warning(f"Download failed: {str(e)}. Check your network (firewall, VPN, DNS), ensure the URL is valid, or upload a file.")
        return None

# Function to extract audio
def extract_audio(video_path, output_path="temp_audio.wav"):
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(output_path)
        video.audio.close()
        video.close()
        return output_path
    except Exception as e:
        st.error(f"Error extracting audio: {str(e)}")
        return None

# Function to transcribe audio
def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None

# Function to classify accent
def classify_accent(audio_path):
    try:
        # Define a user-writable savedir
        savedir = "./pretrained_models/accent-id-commonaccent_ecapa"
        os.makedirs(savedir, exist_ok=True)  # Create directory if it doesn't exist
        
        # Load ECAPA-TDNN model
        classifier = sb.EncoderClassifier.from_hparams(
            source="Jzuluaga/accent-id-commonaccent_ecapa",
            savedir=savedir
        )
        # Classify the audio file
        out_prob, score, index, text_lab = classifier.classify_file(audio_path)
        accent = text_lab[0]  # e.g., "us", "england", "australia"
        confidence = float(score[0]) * 100  # Convert to percentage
        # Map accent codes to readable names
        accent_map = {
            "us": "American", "england": "British", "australia": "Australian",
            "canada": "Canadian", "indian": "Indian", "ireland": "Irish",
            "scotland": "Scottish", "newzealand": "New Zealand", "wales": "Welsh",
            "african": "African", "bermuda": "Bermudian", "hongkong": "Hong Kong",
            "malaysia": "Malaysian", "philippines": "Filipino", "singapore": "Singaporean",
            "southatlandtic": "South Atlantic"
        }
        accent = accent_map.get(accent.lower(), accent)
        return accent, confidence
    except Exception as e:
        st.error(f"Error classifying accent: {str(e)}")
        return None, None

# Streamlit UI
st.title("English Accent Analyzer")
st.write("Enter a public MP4 video URL or upload an MP4 file to analyze the speaker's English accent.")
st.write("**Recommended**: Upload an MP4 file to avoid network issues. For URLs, use direct MP4 links (e.g., 'https://filesamples.com/samples/video/mp4/sample_960x400_ocean_with_audio.mp4') or Google Drive shared links set to 'Anyone with the link'.")

# Input options: URL or file upload
video_url = st.text_input("Enter Video URL (e.g., direct MP4 or Google Drive shared link):")
uploaded_file = st.file_uploader("Or upload a video file (MP4):", type=["mp4"])

if st.button("Analyze"):
    if not check_ffmpeg():
        st.stop()

    with st.spinner("Processing..."):
        video_path = None
        audio_path = None

        # Handle file upload first
        if uploaded_file:
            try:
                video_path = os.path.join(tempfile.gettempdir(), "uploaded_video.mp4")
                with open(video_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                st.write(f"Uploaded file saved to: {video_path}")
            except Exception as e:
                st.error(f"Error saving uploaded file: {str(e)}")
                st.stop()

        # Handle URL if no file is uploaded
        elif video_url:
            video_path = download_video(video_url)
            if not video_path:
                st.error("Failed to download video. Ensure the URL is a direct MP4 or public Google Drive link, check your network, or upload a file.")
                st.stop()

        else:
            st.error("Please provide a valid video URL or upload a file.")
            st.stop()

        # Extract audio
        if video_path and os.path.exists(video_path):
            audio_path = extract_audio(video_path)
            if audio_path and os.path.exists(audio_path):
                # Transcribe audio
                transcription = transcribe_audio(audio_path)
                if transcription:
                    # Classify accent
                    accent, confidence = classify_accent(audio_path)
                    if accent and confidence:
                        st.success("Analysis Complete!")
                        st.write(f"**Detected Accent**: {accent}")
                        st.write(f"**Confidence Score**: {confidence:.2f}%")
                        st.write("**Summary**: The audio was transcribed to confirm English speech, and the accent was classified using the ECAPA-TDNN model trained on the CommonAccent dataset, supporting 16 English accents.")
                    else:
                        st.error("Accent classification failed.")
                else:
                    st.error("Transcription failed.")
                # Clean up
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            else:
                st.error("Audio extraction failed.")
            # Clean up video file
            if os.path.exists(video_path):
                os.remove(video_path)
        else:
            st.error("Video file not found or invalid.")
