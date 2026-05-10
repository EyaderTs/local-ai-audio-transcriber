from fastapi import FastAPI, UploadFile
from faster_whisper import WhisperModel
import tempfile
import os

app = FastAPI()

print("Loading Whisper model... Please wait.")

model = WhisperModel(
    "tiny",
    device="auto",
    compute_type="int8"
)

print("Whisper model fully loaded!")


@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile):

    content = await audio.read()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:

        tmp.write(content)
        tmp_path = tmp.name

    try:

        segments, _ = model.transcribe(tmp_path)

        text = " ".join(
            segment.text for segment in segments
        )

        return {
            "text": text
        }

    finally:

        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.get("/")
def health():
    return {"message": "Hello from FastAPI"}