import requests
import pandas as pd
from typing import Dict, Optional, List
from dotenv import load_dotenv
import os
import yfinance as yf
from datetime import datetime, timedelta
import time

# Load environment variables from .env file
load_dotenv()

class AlphaVantageStock:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ALPHA_VANTAGE_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set ALPHA_VANTAGE_API_KEY in .env file")
        self.base_url = "https://www.alphavantage.co/query"

    def get_overview(self, symbol: str) -> Dict:
        """Fetch company overview data"""
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_earnings(self, symbol: str) -> Dict:
        """Fetch earnings data"""
        params = {
            "function": "EARNINGS",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_income_statement(self, symbol: str) -> Dict:
        """Fetch income statement data"""
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_balance_sheet(self, symbol: str) -> Dict:
        """Fetch balance sheet data"""
        params = {
            "function": "BALANCE_SHEET",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_cash_flow(self, symbol: str) -> Dict:
        """Fetch cash flow data"""
        params = {
            "function": "CASH_FLOW",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_global_quote(self, symbol: str) -> Dict:
        """Fetch real-time quote data"""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_stock_metrics(self, symbol: str) -> Dict[str, Optional[float]]:
        """Get comprehensive stock metrics"""
        # Fetch all data from Alpha Vantage
        overview = self.get_overview(symbol)
        earnings = self.get_earnings(symbol)
        income = self.get_income_statement(symbol)
        balance = self.get_balance_sheet(symbol)
        cash_flow = self.get_cash_flow(symbol)
        quote = self.get_global_quote(symbol)

        # Extract key metrics
        metrics = {
            # Valuation Metrics
            'Market Cap (B)': float(overview.get('MarketCapitalization', 0)) / 1e9 if overview.get('MarketCapitalization') else None,
            'P/E Ratio': float(overview.get('PERatio', 0)) if overview.get('PERatio') else None,
            'P/B Ratio': float(overview.get('PriceToBookRatio', 0)) if overview.get('PriceToBookRatio') else None,
            'P/S Ratio': float(overview.get('PriceToSalesRatioTTM', 0)) if overview.get('PriceToSalesRatioTTM') else None,
            
            # Profitability Metrics
            'ROE (%)': float(overview.get('ReturnOnEquityTTM', 0)) if overview.get('ReturnOnEquityTTM') else None,
            'ROA (%)': float(overview.get('ReturnOnAssetsTTM', 0)) if overview.get('ReturnOnAssetsTTM') else None,
            'Profit Margin (%)': float(overview.get('ProfitMargin', 0)) if overview.get('ProfitMargin') else None,
            
            # Growth Metrics
            'Revenue Growth (%)': float(overview.get('QuarterlyRevenueGrowthYOY', 0)) if overview.get('QuarterlyRevenueGrowthYOY') else None,
            'EPS Growth (%)': float(overview.get('QuarterlyEarningsGrowthYOY', 0)) if overview.get('QuarterlyEarningsGrowthYOY') else None,
            
            # Dividend Metrics
            'Dividend Yield (%)': float(overview.get('DividendYield', 0)) if overview.get('DividendYield') else None,
            'Dividend Payout Ratio (%)': float(overview.get('PayoutRatio', 0)) if overview.get('PayoutRatio') else None,
            
            # Financial Health
            'Debt/Equity': float(overview.get('DebtToEquity', 0)) if overview.get('DebtToEquity') else None,
            'Current Ratio': float(overview.get('CurrentRatio', 0)) if overview.get('CurrentRatio') else None,
            
            # Price Information
            'Current Price': float(quote.get('Global Quote', {}).get('05. price', 0)) if quote.get('Global Quote') else None,
            '52 Week High': float(overview.get('52WeekHigh', 0)) if overview.get('52WeekHigh') else None,
            '52 Week Low': float(overview.get('52WeekLow', 0)) if overview.get('52WeekLow') else None,
        }

        # Calculate 5Y CAGR from earnings
        if 'annualEarnings' in earnings:
            annual_earnings = earnings['annualEarnings']
            if len(annual_earnings) >= 5:
                current_eps = float(annual_earnings[0]['reportedEPS'])
                past_eps = float(annual_earnings[4]['reportedEPS'])
                if past_eps > 0:
                    metrics['5Y CAGR (%)'] = ((current_eps / past_eps) ** (1/5) - 1) * 100

        return metrics

    def get_yfinance_supplement(self, symbol: str) -> Dict:
        """Get additional data from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            return {
                'Beta': info.get('beta'),
                'Forward P/E': info.get('forwardPE'),
                'PEG Ratio': info.get('pegRatio'),
                'Enterprise Value (B)': info.get('enterpriseValue', 0) / 1e9 if info.get('enterpriseValue') else None,
                'Enterprise Value/EBITDA': info.get('enterpriseToEbitda'),
                'Free Cash Flow (B)': info.get('freeCashflow', 0) / 1e9 if info.get('freeCashflow') else None,
                'Operating Cash Flow (B)': info.get('operatingCashflow', 0) / 1e9 if info.get('operatingCashflow') else None,
                'Revenue Growth (3Y)': info.get('revenueGrowth'),
                'Earnings Growth (3Y)': info.get('earningsGrowth'),
                'Analyst Target Price': info.get('targetMeanPrice'),
                'Analyst Recommendation': info.get('recommendationMean'),
                'Short % of Float': info.get('shortPercentOfFloat'),
                'Institution %': info.get('heldPercentInstitutions'),
                'Insider %': info.get('heldPercentInsiders'),
            }
        except Exception as e:
            print(f"Error fetching yfinance data for {symbol}: {e}")
            return {}

def main():
    # Example usage
    stock_analyzer = AlphaVantageStock()
    
    # Example stocks (replace with your desired stocks)
    stocks = ['AAPL', 'MSFT', 'GOOGL']
    
    results = {}
    for symbol in stocks:
        print(f"Fetching data for {symbol}...")
        
        # Get Alpha Vantage data
        metrics = stock_analyzer.get_stock_metrics(symbol)
        
        # Get Yahoo Finance supplement
        yf_data = stock_analyzer.get_yfinance_supplement(symbol)
        
        # Combine all data
        combined_data = {**metrics, **yf_data}
        results[symbol] = combined_data
        
        # Be kind to the APIs
        time.sleep(1)
    
    # Convert to DataFrame for better visualization
    df = pd.DataFrame(results).T
    
    # Format the DataFrame
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.float_format', '{:.2f}'.format)
    
    print("\nComprehensive Stock Metrics:")
    print(df)

if __name__ == "__main__":
    main() 