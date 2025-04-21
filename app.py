from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import re

# Load API key ONLY from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")  # No fallbacks

if not api_key:
    raise ValueError("API key missing - add GEMINI_API_KEY to .env")

# Configure Gemini (using 1.0 Pro for better free tier limits)
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    try:
        # Attempt API call with timeout
        response = model.generate_content(
            user_input,
            request_options={'timeout': 10}  # 10-second timeout
        )
        return jsonify({'response': response.text})
        
    except Exception as e:
        error_msg = str(e)
        
        # Handle rate limits with humor
        if "429" in error_msg:
            wait_time = re.search(r'retry_delay.*?(\d+)', error_msg)
            return jsonify({
                'response': f"🎤 <b>Comedy Club Rules:</b> Only 2 jokes/minute allowed! "
                          f"Wait {wait_time.group(1) if wait_time else '30'} seconds "
                          f"before your next performance!",
                'wait_seconds': int(wait_time.group(1)) if wait_time else 30
            }), 429
            
        # General error handling    
        return jsonify({
            'response': "🤖 <b>Technical Difficulties:</b> My joke circuits are overloaded! "
                       "Try again in a moment!"
        }), 500

# Vercel handler remains unchanged
def vercel_handler(request):
    with app.app_context():
        return app.full_dispatch_request()()

if __name__ == '__main__':
    app.run(debug=True)