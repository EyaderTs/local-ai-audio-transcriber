# Local AI Audio Transcriber

A full-stack AI-powered audio transcription app built with:

- FastAPI (Python backend)
- React + Vite + TypeScript (frontend)
- Faster-Whisper for speech-to-text
- Ollama for local LLM text cleaning
- Docker & Docker Compose

The app can:

- Record audio from the browser
- Upload audio files
- Transcribe speech into text
- Clean and improve transcripts using a local LLM

---

# Project Structure

```bash
local-ai-audio-transcriber/
├── backend/
├── frontend/
├── docker-compose.yml
└── README.md
```

---

# Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/EyaderTs/local-ai-audio-transcriber.git
cd local-ai-audio-transcriber
```

---

## 2. Install Requirements

### Install Docker Desktop

Download here:
https://www.docker.com/products/docker-desktop/

Check installation:

```bash
docker --version
docker compose version
```

---

### Install Ollama

Download Ollama:
https://ollama.com/download

Check:

```bash
ollama --version
```

---

## 3. Pull the AI model

This project uses:

```bash
llama3.2:3b
```

Pull it:

```bash
ollama pull llama3.2:3b
```

Verify:

```bash
ollama list
```

---

## 4. Start Ollama

Make sure Ollama is running:

```bash
ollama serve
```

(or just open the Ollama app)

---

## 5. Configure environment

Create a file:

```bash
backend/.env
```

Add:

```env
LLM_BASE_URL=http://host.docker.internal:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=llama3.2:3b
WHISPER_MODEL=base
```

---

## 6. Run the application

From the root folder:

```bash
docker compose up --build
```

---

## 7. Open the app

Frontend:

```
http://localhost:3000
```

Backend API Docs:

```
http://localhost:8000/docs
```

---

## 8. Stop the app

```bash
docker compose down
```

---

# How it works (simple explanation)

- Frontend (React) handles UI and audio recording
- Backend (FastAPI) handles:
  - Whisper transcription
  - LLM cleaning
- Ollama runs locally on your machine
- Docker connects everything together

Backend communicates with Ollama via:

```
http://host.docker.internal:11434/v1
```

---

# Features

- Voice recording in browser
- Audio file upload
- Whisper transcription
- LLM text cleaning (Ollama)
- Fully Dockerized setup
- Fast local inference

---

# Notes

- First run may take time (model download)
- Whisper model downloads automatically
- Ollama model must be pulled manually
- This setup is optimized for local development

---
