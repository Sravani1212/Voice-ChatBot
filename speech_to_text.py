from google.cloud import speech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/google-cloud-credentials.json"

speech_client = speech.SpeechClient()

def speech_to_text(audio_file):
    with open(audio_file, "rb") as audio:
        audio_content = audio.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = speech_client.recognize(config=config, audio=audio)

    for result in response.results:
        return result.alternatives[0].transcript
