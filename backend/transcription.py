from faster_whisper import WhisperModel
from openai import OpenAI
from pathlib import Path

# Edit system_prompt.txt to change how the LLM cleans transcriptions
PROMPT_FILE = Path(__file__).parent / "system_prompt.txt"
SYSTEM_PROMPT = PROMPT_FILE.read_text().strip()

class TranscriptionService:

    def __init__(self, whisper_model, llm_base_url, llm_api_key, llm_model):

        print("Loading Whisper model...")

        self.whisper = WhisperModel(
            whisper_model,
            device="auto",
            compute_type="int8"
        )
        self.llm_client = OpenAI(
            base_url=llm_base_url,
            api_key=llm_api_key
        )
        self.llm_model = llm_model
        print("Whisper loaded!")

    def transcribe(self, audio_file):

        print("Transcribing audio...")

        segments, info = self.whisper.transcribe(
            audio_file, beam_size=5, language="en", condition_on_previous_text=False
        )

        text = " ".join([segment.text for segment in segments]).strip()
        print(f"📝 Raw: {text}")

        return text

    def clean_with_llm(self, text, system_prompt=None):
        if not text:
            return ""

        # Use custom prompt or fall back to default
        prompt_to_use = system_prompt if system_prompt else SYSTEM_PROMPT

        print("🤖 Cleaning with LLM...")

        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": prompt_to_use},
                    {"role": "user", "content": text},
                ],
                temperature=0.3,
                max_tokens=200,
            )

            cleaned = response.choices[0].message.content.strip()
            print(f"✨ Cleaned: {cleaned}")
            return cleaned

        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            return text  # Fallback to raw text
