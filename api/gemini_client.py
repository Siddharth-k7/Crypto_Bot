import google.generativeai as genai
from typing import Dict, Optional
import traceback

class GeminiClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        try:
            genai.configure(api_key=api_key)
            # Updated model name - use gemini-1.5-flash instead of gemini-pro
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print(f"✅ Gemini configured with API key: {api_key[:10]}...")
        except Exception as e:
            print(f"❌ Gemini configuration failed: {e}")
            raise
    
    def get_crypto_response(self, user_message: str, crypto_data: Dict) -> Optional[str]:
        try:
            context = self._format_crypto_context(crypto_data)
            print(f"🔵 Crypto context: {context}")
            
            prompt = f"""
            As a cryptocurrency expert assistant, answer the user's question using this real-time data:
            
            {context}
            
            User Question: {user_message}
            
            Provide a helpful, accurate response. Include current prices and market data when relevant.
            Keep the response concise and mention that crypto investments carry risks.
            """
            
            print(f"🔵 Sending prompt to Gemini...")
            response = self.model.generate_content(prompt)
            print(f"✅ Gemini response received")
            return response.text
            
        except Exception as e:
            print(f"❌ Gemini crypto response error: {e}")
            traceback.print_exc()
            return f"Sorry, I encountered an error: {str(e)}"
    
    def get_general_crypto_response(self, user_message: str) -> Optional[str]:
        try:
            prompt = f"""
            As a cryptocurrency education assistant, answer this question: {user_message}
            
            Provide educational, balanced information about cryptocurrency and blockchain technology.
            Include relevant examples and always mention risks associated with crypto investments.
            Keep the response informative but concise.
            """
            
            print(f"🔵 Sending general prompt to Gemini...")
            response = self.model.generate_content(prompt)
            print(f"✅ Gemini general response received")
            return response.text
            
        except Exception as e:
            print(f"❌ Gemini general response error: {e}")
            traceback.print_exc()
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _format_crypto_context(self, crypto_data: Dict) -> str:
        if not crypto_data:
            return "No current crypto data available."
            
        context_parts = []
        
        for coin_id, data in crypto_data.items():
            if coin_id == 'trending':
                if data:
                    trending_names = [coin['item']['name'] for coin in data]
                    context_parts.append(f"Trending: {', '.join(trending_names)}")
            elif coin_id == 'market_overview':
                if data:
                    market_info = []
                    for coin in data[:3]:
                        market_info.append(f"{coin['name']}: ${coin['current_price']:.2f}")
                    context_parts.append(f"Market Leaders: {' | '.join(market_info)}")
            else:
                if isinstance(data, dict) and 'usd' in data:
                    price = data['usd']
                    change = data.get('usd_24h_change', 0)
                    context_parts.append(f"{coin_id.title()}: ${price:.2f} ({change:+.2f}%)")
        
        return " | ".join(context_parts) if context_parts else "No crypto data available."
