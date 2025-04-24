import requests
import pandas as pd
from typing import Dict, Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class AlphaVantageStock:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ALPHA_VANTAGE_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set ALPHA_VANTAGE_API_KEY in .env file")
        self.base_url = "https://www.alphavantage.co/query"

    def get_overview(self, symbol: str) -> Dict:
        """Fetch company overview data including ROE and Dividend Yield"""
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_earnings(self, symbol: str) -> Dict:
        """Fetch earnings data including growth rates"""
        params = {
            "function": "EARNINGS",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_stock_metrics(self, symbol: str) -> Dict[str, Optional[float]]:
        """Get ROE, 5Y CAGR, and Dividend Yield for a given stock"""
        overview = self.get_overview(symbol)
        earnings = self.get_earnings(symbol)

        # Extract ROE from overview
        roe = float(overview.get('ReturnOnEquityTTM', 0)) if overview.get('ReturnOnEquityTTM') else None

        # Extract Dividend Yield from overview
        div_yield = float(overview.get('DividendYield', 0)) if overview.get('DividendYield') else None

        # Calculate 5Y CAGR from earnings
        cagr = None
        if 'annualEarnings' in earnings:
            annual_earnings = earnings['annualEarnings']
            if len(annual_earnings) >= 5:
                current_eps = float(annual_earnings[0]['reportedEPS'])
                past_eps = float(annual_earnings[4]['reportedEPS'])
                if past_eps > 0:
                    cagr = ((current_eps / past_eps) ** (1/5) - 1) * 100

        return {
            'ROE (%)': roe,
            '5Y CAGR (%)': cagr,
            'Dividend Yield (%)': div_yield
        }

def main():
    # Example usage
    stock_analyzer = AlphaVantageStock()
    
    # Example stocks (replace with your desired stocks)
    stocks = ['AAPL', 'MSFT', 'GOOGL']
    
    results = {}
    for symbol in stocks:
        print(f"Fetching data for {symbol}...")
        metrics = stock_analyzer.get_stock_metrics(symbol)
        results[symbol] = metrics
    
    # Convert to DataFrame for better visualization
    df = pd.DataFrame(results).T
    print("\nStock Metrics:")
    print(df)

if __name__ == "__main__":
    main() 