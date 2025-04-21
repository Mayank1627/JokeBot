import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("API key missing — make sure OPENROUTER_API_KEY is set in .env")

# OpenRouter Gemini model endpoint
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "google/gemini-pro",  # OpenRouter model name for Gemini Pro
    "messages": [
        {"role": "user", "content": "Tell me a programming joke"}
    ],
    "max_tokens": 200
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    output = response.json()
    print("\n✅ Response:\n", output['choices'][0]['message']['content'])

except requests.exceptions.HTTPError as http_err:
    print(f"\n❌ HTTP error occurred: {http_err}")
    print("🔍 Response details:", response.text)
except Exception as err:
    print(f"\n❌ Other error occurred: {err}")
