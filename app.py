from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load OpenRouter API Key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("Missing OPENROUTER_API_KEY in environment variables!")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "google/gemini-pro",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are JokeGPT, a hilarious AI comedian. "
                    "Always respond with a funny joke, witty comeback, or humorous story based on the user's message. "
                    "Your tone should be lighthearted, playful, and entertaining."
                )
            },
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 200
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers, json=data)
        response.raise_for_status()
        output = response.json()
        return jsonify({'response': output['choices'][0]['message']['content']})

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 429:
            return jsonify({
                'response': "🎤 <b>Too many requests:</b> You're telling jokes too fast! Slow down! ⏳",
            }), 429
        return jsonify({
            'response': f"❌ <b>Error:</b> {http_err}"
        }), 500

    except Exception as err:
        return jsonify({
            'response': f"🤖 <b>Oops!</b> Something went wrong: {err}"
        }), 500


# For Vercel (if using it)
def vercel_handler(request):
    with app.app_context():
        return app.full_dispatch_request()()

if __name__ == '__main__':
    app.run(debug=True)
