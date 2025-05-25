# English Accent Analyzer

This project is a Streamlit web application that analyzes English accents from MP4 video files. It accepts a public MP4 video URL (direct MP4 or Google Drive shared link) or an uploaded MP4 file, extracts the audio, transcribes it using Whisper, and classifies the speaker's English accent using the ECAPA-TDNN model (`Jzuluaga/accent-id-commonaccent_ecapa`, 87% accuracy on 16 English accents). The app outputs the detected accent (e.g., "British", "American", "Australian") and a confidence score.

## Features
- **Input Options**: Supports direct MP4 URLs, Google Drive shared links (set to "Anyone with the link"), and MP4 file uploads.
- **Audio Processing**: Extracts audio from MP4 videos using `moviepy` and `ffmpeg`.
- **Transcription**: Uses Whisper (`tiny` model) to transcribe audio, ensuring English speech.
- **Accent Classification**: Identifies one of 16 English accents using the ECAPA-TDNN model, mapping codes (e.g., "us") to readable names (e.g., "American").
- **Robust Downloading**: Handles URLs with `requests`, including `User-Agent` headers, 120-second timeout, and 5 retries for HTTP 403, 429, 500, 502, 503, 504 errors.
- **User-Friendly UI**: Streamlit interface with clear instructions and error messages.
- **Cleanup**: Deletes temporary video and audio files after processing.

## Setup
Follow these steps to set up the project locally.

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd accent-analyzer
