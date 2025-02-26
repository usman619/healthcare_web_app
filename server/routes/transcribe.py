from fastapi import FastAPI, File, HTTPException, APIRouter, UploadFile
from dotenv import load_dotenv
from pydub import AudioSegment
import speech_recognition as sr
from google import genai
import os
import io
import tempfile

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

router = APIRouter(
    prefix="/transcribe",
    tags=["Transcription"]
)

@router.post("/")
async def transcribe_audio(file: UploadFile = File(...)):
    allowed_formats = ['audio/wav', 'audio/x-wav', 'audio/mpeg', 'audio/mp3']
    if file.content_type not in allowed_formats:
        raise HTTPException(status_code=500, detail="Unsupported file format (use WAV or MP3).")
    try:
        audio_bytes = await file.read()

        # Load the audio file as an AudioSegment, converting if needed
        if file.content_type in ['audio/mpeg', 'audio/mp3']:
            with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_mp3:
                temp_mp3.write(audio_bytes)
                temp_mp3.flush()
                sound = AudioSegment.from_file(temp_mp3.name, format="mp3")
        else:
            # For WAV files, load from BytesIO
            sound = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")

        # Define chunk duration (in milliseconds)
        chunk_duration_ms = 20000  # 20 seconds
        overlap_ms = 5000            # 5 seconds overlap

        full_transcript = ""
        recognizer = sr.Recognizer()

        start = 0
        while start < len(sound):
            end = start + chunk_duration_ms
            # Adding a limit to the end of the audio file
            chunk = sound[start:end]
            
            chunk_io = io.BytesIO()
            chunk.export(chunk_io, format="wav")
            chunk_io.seek(0)
            
            with sr.AudioFile(chunk_io) as source:
                audio_data = recognizer.record(source)
            
            try:
                chunk_transcript = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                chunk_transcript = "[inaudible]"
            except sr.RequestError as e:
                raise HTTPException(status_code=500, detail="Speech API error: " + str(e))
            
            full_transcript += chunk_transcript + " "
            start += (chunk_duration_ms - overlap_ms)  # move by chunk duration minus overlap

        full_transcript = full_transcript
        # full_transcript = await transcribe_check(full_transcript)
        return {"transcript": full_transcript}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def transcribe_check(transcript: str):
    # check if the grammer and medical terms are correct for the transcript using the gemini API
    prompt = (
    f"Please correct the grammar, punctuation, and medical terminology of the following transcript. "
    f"Return only the corrected transcript text without any explanations or commentary:\n"
    f"{transcript}"
    )

    try:
        client = genai.Client(api_key=gemini_api_key)

        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
            
            )
        
        transcript_check = response.text
        return transcript_check
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))