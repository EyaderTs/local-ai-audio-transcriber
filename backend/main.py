from fastapi import FastAPI,UploadFile
import tempfile
import os

app= FastAPI()


@app.post("/transcribe")
async def transcribe_audio(audio:UploadFile):

    content = await audio.read()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    
    try:     
        return{
            "name":audio.filename,
            "temp_file":tmp_path    
        }

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
    
@app.get("/")
def health():
    return {"Message":"Hello from FastAPI"}