from fastapi import File, HTTPException, APIRouter, UploadFile
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
            # Create a temporary MP3 file that ffmpeg can access
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
                temp_mp3.write(audio_bytes)
                temp_mp3.flush()
                temp_mp3.seek(0)  # Reset pointer before reading
                sound = AudioSegment.from_file(temp_mp3.name, format="mp3")
                print("Audio duration (seconds):", len(sound) / 1000.0)
            os.remove(temp_mp3.name)  # Clean up the temporary file
        else:
            # For WAV files, load directly from an in-memory buffer
            sound = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
            print("Audio duration (seconds):", len(sound) / 1000.0)


        # Define chunk duration (in milliseconds) and overlap
        chunk_duration_ms = 20000  # 20 seconds
        overlap_ms = 5000          # 5 seconds overlap

        full_transcript = ""
        recognizer = sr.Recognizer()

        start = 0
        while start < len(sound):
            end = start + chunk_duration_ms
            chunk = sound[start:end]
            
            # Export chunk to a BytesIO buffer and reset pointer
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
            start += (chunk_duration_ms - overlap_ms)

        original_transcript = full_transcript.strip()
        # Optionally, post-process the transcript with the Gemini API
        checked_transcript = await transcribe_check(original_transcript)
        return {
            "transcript_original": original_transcript,
            "transcript_checked": checked_transcript
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def transcribe_check(transcript: str):
    prompt = (
        f"Please correct the grammar, punctuation, and medical terminology of the following transcript."
        f"Return only the corrected transcript text without any explanations or commentary or summarizing it:\n"
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
