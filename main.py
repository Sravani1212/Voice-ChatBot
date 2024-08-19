import sounddevice as sd
import wavio
import openai
import time
import os
from google.cloud import speech
from openai.error import RateLimitError, InvalidRequestError
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Initialize Google Cloud Speech-to-Text
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/google-cloud-credentials.json"
speech_client = speech.SpeechClient()

# Set your OpenAI API key here
openai.api_key = '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'


# Audio recording parameters
FORMAT = 'int16'
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

# Google Calendar API setup
credentials = service_account.Credentials.from_service_account_file(
    'credentials/service-account-file.json',
    scopes=['https://www.googleapis.com/auth/calendar']
)
calendar_service = build('calendar', 'v3', credentials=credentials)

def create_appointment(summary, start_time, end_time):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'America/Los_Angeles'},
        'end': {'dateTime': end_time, 'timeZone': 'America/Los_Angeles'},
    }
    event = calendar_service.events().insert(calendarId='primary', body=event).execute()
    return event

def record_audio(filename):
    print("Recording...")
    audio = sd.rec(int(RECORD_SECONDS * RATE), samplerate=RATE, channels=CHANNELS, dtype=FORMAT)
    sd.wait()  # Wait until recording is finished
    wavio.write(filename, audio, RATE, sampwidth=2)
    print("Recording finished.")

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

def generate_response(prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message['content'].strip()
        except RateLimitError as e:
            print(f"Rate limit exceeded, retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)
        except InvalidRequestError as e:
            print(f"Invalid request: {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
    raise Exception("Rate limit exceeded and retries failed.")

def main():
    while True:
        # Step 1: Record and transcribe the user's request
        record_audio("audio/input_mono.wav")
        user_input = speech_to_text("audio/input_mono.wav")
        print("User said:", user_input)

        # Step 2: Check if the user wants to make an appointment
        if "appointment" in user_input.lower():
            # Ask for name
            print("Bot: What is your name?")
            record_audio("audio/input_mono.wav")
            name = speech_to_text("audio/input_mono.wav")
            print("User said:", name)

            # Ask for the reason
            print("Bot: What is the reason for the appointment?")
            record_audio("audio/input_mono.wav")
            reason = speech_to_text("audio/input_mono.wav")
            print("User said:", reason)

            # Ask for the preferred date and time
            print("Bot: What is your preferred date and time for the appointment?")
            record_audio("audio/input_mono.wav")
            preferred_time = speech_to_text("audio/input_mono.wav")
            print("User said:", preferred_time)

            # Generate response based on provided details
            prompt = f"Schedule an appointment for {name} regarding {reason} at their preferred time: {preferred_time}."
            response = generate_response(prompt)
            print("Bot response:", response)

            # Assume some dummy appointment options
            options = [
                ("2023-08-07T10:00:00-07:00", "2023-08-07T11:00:00-07:00"),
                ("2023-08-07T12:00:00-07:00", "2023-08-07T13:00:00-07:00"),
                ("2023-08-07T14:00:00-07:00", "2023-08-07T15:00:00-07:00")
            ]

            # Present options to the user
            print("Bot: Here are a few options for your appointment:")
            for i, option in enumerate(options, 1):
                print(f"Option {i}: {option[0]} to {option[1]}")

            # Ask the user to choose an option
            print("Bot: Please choose an option by saying the option number.")
            record_audio("audio/input_mono.wav")
            option_choice = speech_to_text("audio/input_mono.wav")
            print("User said:", option_choice)

            # Convert option choice to index
            try:
                option_index = int(option_choice.split()[-1]) - 1
                chosen_option = options[option_index]

                # Create the appointment with the chosen option
                summary = f"Appointment for {name}"
                start_time, end_time = chosen_option
                event = create_appointment(summary, start_time, end_time)
                
                # Print the created appointment details
                print(f"Appointment created:\nTime: {start_time} to {end_time}\nPlace: Car Showroom")
            except (IndexError, ValueError):
                print("Bot: Invalid option chosen. Please try again.")
        else:
            # General response for non-appointment related queries
            prompt = f"The user said: '{user_input}'. Respond as a car showroom assistant."
            response = generate_response(prompt)
            print("Bot response:", response)

if __name__ == "__main__":
    main()
