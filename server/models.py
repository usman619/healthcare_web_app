from pydantic import BaseModel

class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str