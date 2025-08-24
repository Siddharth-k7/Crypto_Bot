import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests

load_dotenv()

# Test Gemini API
print("🔵 Testing Gemini API...")
try:
    gemini_key = os.getenv('GEMINI_API_KEY')
    print(f"Gemini API Key: {gemini_key[:10]}...")
    
    genai.configure(api_key=gemini_key)
    # Use the updated model name
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print(f"✅ Gemini works: {response.text}")
except Exception as e:
    print(f"❌ Gemini failed: {e}")

# Test CoinGecko API
print("\n🔵 Testing CoinGecko API...")
try:
    coingecko_key = os.getenv('COINGECKO_API_KEY')
    print(f"CoinGecko API Key: {coingecko_key[:10]}...")
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {'x-cg-demo-api-key': coingecko_key} if coingecko_key else {}
    params = {'ids': 'bitcoin', 'vs_currencies': 'usd'}
    
    response = requests.get(url, headers=headers, params=params)
    print(f"✅ CoinGecko works: {response.json()}")
except Exception as e:
    print(f"❌ CoinGecko failed: {e}")
