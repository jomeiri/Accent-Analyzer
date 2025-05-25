# English Accent Analyzer

This project is a Streamlit web application that analyzes English accents from MP4 video files. It accepts a public MP4 video URL (direct MP4 or Loom) or an uploaded MP4 file, extracts the audio, transcribes it using Whisper, and classifies the speaker's English accent using the ECAPA-TDNN model (`Jzuluaga/accent-id-commonaccent_ecapa`, 87% accuracy on 16 English accents). The app outputs the detected accent (e.g., "British", "American", "Australian") and a confidence score.

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

- **Create a Virtual Environment (recommended)**:
  ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
- **Install Dependencies**:
Ensure Python 3.8+ is installed. Then, install the required packages:
  ```bash
   pip install -r requirements.txt
- **Install ffmpeg**:
- Windows:
Download from ffmpeg.org.

Extract and add the bin folder to your system PATH (e.g., C:\ffmpeg\bin).

Alternatively, install via Chocolatey: choco install ffmpeg.
- MacOS:
Install via Homebrew: brew install ffmpeg.

- Linux:
Install via package manager, e.g., sudo apt-get install ffmpeg (Ubuntu/Debian).

- **Verify installation**:
  ```bash
  ffmpeg -version.

- **Run the App**
Start the Streamlit Server:
  ```bash
  streamlit run accent_analyzer.py
This opens the app in your default browser at http://localhost:8501.

Interact with the App:
URL Input: Enter a public MP4 video URL (direct MP4 or Loom).

File Upload: Upload an MP4 file via the file uploader.

Click the "Analyze" button to process the video and view results.



