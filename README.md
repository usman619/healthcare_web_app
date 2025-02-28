# Healthcare Translation Web App 🏥

A FastAPI and Streamlit–based application that provides real-time medical transcription and translation services.

## Features 🌟

- **Audio Input & Processing**
  - Real-time voice recording via microphone
  - Support for both WAV and MP3 file uploads
  - Chunked audio processing for long recordings
  - Audio duration validation

- **Transcription Capabilities**
  - Speech-to-text conversion with real-time feedback
  - Medical terminology validation
  - Grammar and punctuation correction
  - Support for multiple audio formats

- **Translation Services**
  - Multi-language support (11+ languages)
  - Medical context–aware translations
  - Real-time translation processing
  - Customizable source and target language selection

- **Audio Output**
  - Text-to-speech conversion for translated text
  - Downloadable translated audio
  - Audio playback controls
  - Support for multiple accents

- **User Interface**
  - Mobile-responsive design
  - Dual transcript display (original and corrected)
  - Real-time processing indicators
  - Intuitive language selection

## Architecture 🏗️

```mermaid
graph LR
    subgraph Client
      A[Streamlit Web App]
    end

    subgraph Server
      B[FastAPI Server]
    end

    subgraph External_Services
      C[Google Speech Recognition]
      D[Google Gemini AI]
    end

    A -->|Uploads/Records Audio 
         & Text| B
    B -->|Processes Audio| C
    B -->|Post-processes transcript /
     Translates text| D
    C --> B
    D --> B
    B -->|Returns Transcripts
     & Translation| A

```

## Tech Stack 🛠️

- **Backend Framework**: FastAPI
- **AI Services**: 
  - Google Speech Recognition
  - Google Gemini AI
- **Audio Processing**: pydub
- **Frontend: Streamlit**: Streamlit
- **Environment**: Python 3.8+

## Project Structure 📁

```
healthcare_translation_web_app/
├── server/
│   ├── routes/
│   │   ├── transcribe.py      # Audio transcription endpoint
│   │   └── translate.py       # Translation endpoint
│   └── server.py              # Main server configuration
├── streamlit_app/
│   ├── components/
│   │   ├── audio_input.py     # Audio input options (record/upload)
│   │   ├── transcription.py   # Calls transcription API
│   │   └── translation.py     # Calls translation API
│   ├── utils/
│   │   └── config.py          # Configuration constants (e.g., API_BASE_URL)
│   └── app.py                 # Main Streamlit app
├── .env                       # Environment variables
└── README.md                  # Project documentation
```

## API Endpoints 🔌

### Transcription

```http
POST /transcribe/
```

- Accepts WAV/MP3 audio files
- Returns original and corrected transcripts
- Handles medical terminology validation

### Translation

```http
POST /translate/
```
- Accepts source language, target language, and text to be translated
- Returns the translated text

## Setup & Installation 💻

1. Clone the repository:
```bash
git clone https://github.com/usman619/healthcare_web_app
cd healthcare_web_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install ffmpeg in conda or on your device
```bash
conda install -c conda-forge ffmpeg
```
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Start the server:
```bash
cd server
fastapi dev server.py
```

6. Start the Streamlit app:
```bash
cd ../streamlit_app
streamlit run app.py
```

## Environment Variables 🔐

Required environment variables in `.env`:
- `GEMINI_API_KEY`: Google Gemini AI API key
- `API_BASE_URL`: The base URL of your FastAPI server (including the port)

## API Documentation 📚

Access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment 🖥️
**FastAPI code**: [healthcare_server](https://github.com/usman619/healthcare_server)
**Streamlit code**: [healthcare_streamlit](https://github.com/usman619/healthcare_streamlit)

**Streamlit frontend Link**: https://healthcare-translation-web-app.streamlit.app/

I have deployed this project using [Streamlit](https://streamlit.io/) for the frontend and [Railway](https://railway.com/) for the backend.

Streamlit deployment was simple and but I am having issues with `healthcare_server` deployment. I have tested it by creating docker image and testing it locally and that is working perfectly. The following are the deployment images on `railway.com` and 

- Railway server deployment:
<img src="screenshots/railway_deployment_1.png" alt="railway_deployment_1">
- The main issue is `ffmpeg` not working correctly which is resulting in the APIs not working once deployed:
<img src="screenshots/railway_deployment_2.png" alt="railway_deployment_2">

- Now, testing docker image creating and testing the image locally:
<img src="screenshots/creating_docker_image.png" alt="creating_docker_image">
<img src="screenshots/running_docker_image.png" alt="running_docker_image">

- This is the Healthcare Translation Web App working output:
<img src="screenshots/healtcare_app_1.png" alt="healtcare_app_1">
<img src="screenshots/healtcare_app_2.png" alt="healtcare_app_2">
<img src="screenshots/healtcare_app_3.png" alt="healtcare_app_3">
