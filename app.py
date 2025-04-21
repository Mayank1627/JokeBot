from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load ONLY from .env (no fallbacks)
load_dotenv()  
api_key = os.getenv("GEMINI_API_KEY")  # Only reads from .env

if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

genai.configure(api_key=api_key)  # Single secure reference
model = genai.GenerativeModel('gemini-1.5-pro-latest')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    try:
        response = model.generate_content(
            "You are JOKEGPT. Respond ONLY with jokes to: and must be different everytime" + user_input
        )
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel handler (no key references)
def vercel_handler(request):
    with app.app_context():
        return app.full_dispatch_request()()