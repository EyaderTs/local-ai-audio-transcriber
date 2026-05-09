from fastapi import FastAPI,UploadFile


app= FastAPI()

    
@app.get("/")
def health():
    return {"Message":"Hello from FastAPI"}