# from fastapi import FastAPI, File, HTTPException, APIRouter, UploadFile
# from dotenv import load_dotenv
# from pydub import AudioSegment
# import speech_recognition as sr
# from google import genai
# import os
# import io
# import tempfile

# from streamlit import audio

# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# router = APIRouter(
#     prefix="/transcript",
#     tags=["Transcription"]
# )

# @router.post("/")
# async def transcribe_audio(file: UploadFile = File(...)):
#     allowed_formates = ['audio/wav','audio/x-wav','audio/mpeg','audio/mp3']

#     if file.content_type not in allowed_formates:
#         raise HTTPException(status_code=500, detail="Unsupported file formate (use WAV or MP3).")
#     try:
#         audio_bytes = await file.read();
#         # Convert MP3 to WAV formate
#         if file.content_type in ['audio/mpeg','audio/mp3']:
#             # save the file in a temporary file
#             with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_mp3:
#                 temp_mp3.write(audio_bytes)
#                 temp_mp3.flush()

#                 sound = AudioSegment.from_file(temp_mp3.name, format="mp3")

#                 with tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav:
#                     sound.export(temp_wav.name, format="wav")
#                     recongizer = sr.Recognizer()

#                     with sr.AudioFile(temp_wav.name) as source:
#                         audio_data = recongizer.record(source)
#                     transcript = recongizer.recognize_google(audio_data)

#                     # check if the grammer and medical terms are correct for the transcript
#                     # transcript_check_response = await transcribe_check(transcript)
#                     return {"transcript": transcript}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# async def transcribe_check(transcript: str):
#     # check if the grammer and medical terms are correct for the transcript using the gemini API
#     prompt = (
#         f"Check the following transcript to make sure that the grammer and medical terms are spelled correctly:\n"
#         f"{transcript}"
#     )
#     try:
#         client = genai.Client(api_key=gemini_api_key)

#         response = client.models.generate_content(
#             model="gemini-1.5-flash", 
#             contents=prompt
#             )
        
#         transcript_check = response.text
#         return {"transcript_check": transcript_check}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))