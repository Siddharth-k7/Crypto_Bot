import requests
import json
from typing import Dict, List, Optional

class CoinGeckoAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.coingecko.com/api/v3"
        self.headers = {
            'accept': 'application/json',
            'x-cg-demo-api-key': api_key
        }
    
    def get_coin_price(self, coin_id: str, vs_currency: str = 'usd') -> Optional[Dict]:
        """Get current price of a specific coin"""
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': vs_currency,
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching price data: {e}")
            return None
    
    def get_trending_coins(self) -> Optional[List]:
        """Get trending coins"""
        url = f"{self.base_url}/search/trending"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json().get('coins', [])
        except requests.RequestException as e:
            print(f"Error fetching trending coins: {e}")
            return None
    
    def get_market_data(self, vs_currency: str = 'usd', per_page: int = 10) -> Optional[List]:
        """Get market data for top cryptocurrencies"""
        url = f"{self.base_url}/coins/markets"
        params = {
            'vs_currency': vs_currency,
            'order': 'market_cap_desc',
            'per_page': per_page,
            'page': 1,
            'sparkline': False
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching market data: {e}")
            return None
    
    def search_coins(self, query: str) -> Optional[Dict]:
        """Search for coins by name or symbol"""
        url = f"{self.base_url}/search"
        params = {'query': query}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error searching coins: {e}")
            return None
    
    def get_relevant_data(self, user_query: str) -> Dict:
        """Extract relevant crypto data based on user query"""
        data = {}
        
        # Extract coin mentions from user query
        common_coins = {
            'bitcoin': 'bitcoin', 'btc': 'bitcoin',
            'ethereum': 'ethereum', 'eth': 'ethereum',
            'cardano': 'cardano', 'ada': 'cardano',
            'solana': 'solana', 'sol': 'solana'
        }
        
        query_lower = user_query.lower()
        
        # Check for specific coin mentions
        for mention, coin_id in common_coins.items():
            if mention in query_lower:
                price_data = self.get_coin_price(coin_id)
                if price_data:
                    data[coin_id] = price_data[coin_id]
        
        # If no specific coins mentioned, get general market data
        if not data:
            market_data = self.get_market_data(per_page=5)
            if market_data:
                data['market_overview'] = market_data
        
        # Always include trending coins
        trending = self.get_trending_coins()
        if trending:
            data['trending'] = trending[:3]
        
        return data
