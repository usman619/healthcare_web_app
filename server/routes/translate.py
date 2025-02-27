from fastapi import APIRouter, HTTPException
from server.models import TranslateRequest
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

router = APIRouter(
    prefix="/translate",
    tags=["Translate"]
)

@router.post("/")
async def translate_text(request: TranslateRequest):
    prompt = (
        f"Translate the following text from {request.source_lang} to {request.target_lang}:\n"
        f"{request.text}"
    )
    try:
        client = genai.Client(api_key=gemini_api_key)

        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
            )
        
        translation = response.text
        return {"translation": translation}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))