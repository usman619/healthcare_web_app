from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes import translate, transcript, transcribe

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Disable methods like POST and DELETE
    allow_headers=["*"]
)

app.include_router(translate.router)
app.include_router(transcribe.router)

# Root
@app.get("/")
def root():
    return {"message":"Root Endpoint"}