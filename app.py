from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from api.coingecko import CoinGeckoAPI
from api.gemini_client import GeminiClient
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize API clients
coingecko = CoinGeckoAPI(os.getenv('COINGECKO_API_KEY'))
gemini_client = GeminiClient(os.getenv('GEMINI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Check if the message is crypto related
        crypto_keywords = ['price', 'bitcoin', 'ethereum', 'crypto', 'coin', 'market', 
                           'trading', 'investment', 'blockchain', 'btc', 'eth']
        if any(keyword in user_message.lower() for keyword in crypto_keywords):
            crypto_data = coingecko.get_relevant_data(user_message)
            ai_response = gemini_client.get_crypto_response(user_message, crypto_data)
        else:
            ai_response = gemini_client.get_general_crypto_response(user_message)

        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

