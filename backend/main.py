from fastapi import FastAPI, UploadFile
import tempfile
import os
from transcription import TranscriptionService
from typing import Annotated
from fastapi import File, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()  # Load environment variables from .env file
service = None

class CleanRequest(BaseModel):
    text: str
    system_prompt: str | None = None



@asynccontextmanager
async def lifespan(app: FastAPI):
    global service
    print("🚀 Starting up, initializing application...")

    service = TranscriptionService(
        whisper_model = os.getenv('WHISPER_MODEL'),
        llm_base_url = os.getenv('LLM_BASE_URL'),
        llm_api_key = os.getenv('LLM_API_KEY'),
        llm_model = os.getenv('LLM_MODEL')
    )

    print("✅ Application ready!")

    yield


app = FastAPI(title="AI Transcript App",lifespan=lifespan)

# CORS for localhost development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server (Vite)
        "http://localhost:5173",  # React dev server (Vite alternative port)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
async def get_status():
    return {
        "status" : "ready" if service else "initializing",
        "whisper_model" : os.getenv('WHISPER_MODEL'),
        "llm_base_url" : os.getenv('LLM_BASE_URL'),
        "llm_model" : os.getenv('LLM_MODEL')
    }


@app.get("/api/system-prompt")
async def get_system_prompt():
    if not service:
        raise HTTPException(status_code=503, detail="Service not ready")
    return {"default_prompt": service.get_default_system_prompt()}

@app.post("/api/transcribe")
async def transcribe_audio(audio: Annotated[UploadFile, File()]):
    if not service:
        raise HTTPException(
            status_code=503, detail="Service not ready, still initializing models"
        )

    suffix = os.path.splitext(audio.filename)[1] or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        raw_text = service.transcribe(tmp_path)
        return {"success": True, "text": raw_text}

    except Exception as e:
        print(f"❌ Transcription error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Transcription failed: {str(e)}"
        ) from e

    finally:
        # Always clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.post("/api/clean")
async def clean_text(request: CleanRequest):
    if not service:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        cleaned_text = service.clean_with_llm(
            request.text, system_prompt=request.system_prompt
        )
        return {"success": True, "text": cleaned_text}

    except Exception as e:
        print(f"❌ LLM cleaning error: {e}")
        raise HTTPException(status_code=500, detail=f"Cleaning failed: {str(e)}") from e
@app.get("/")
def health():
    return {"message": "Hello from FastAPI"}