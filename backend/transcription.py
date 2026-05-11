from faster_whisper import WhisperModel


class TranscriptionService:

    def __init__(self):

        print("Loading Whisper model...")

        self.whisper = WhisperModel(
            "tiny",
            device="auto",
            compute_type="int8"
        )

        print("Whisper loaded!")

    def transcribe(self, audio_file):

        print("Transcribing audio...")

        segments, info = self.whisper.transcribe(
            audio_file, beam_size=5, language="en", condition_on_previous_text=False
        )

        text = " ".join([segment.text for segment in segments]).strip()
        print(f"📝 Raw: {text}")

        return text