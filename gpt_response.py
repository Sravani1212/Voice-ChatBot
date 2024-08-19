import openai
import time
from openai.error import RateLimitError

openai.api_key = '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'

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
    raise Exception("Rate limit exceeded and retries failed.")
