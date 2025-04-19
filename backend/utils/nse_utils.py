import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from typing import Dict, Any, List
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NSEFetcher:
    def __init__(self):
        self.base_url = "https://www.nseindia.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    @lru_cache(maxsize=1000)
    def get_ohlc(self, symbol: str) -> Dict[str, Any]:
        """Get OHLC data for a symbol."""
        try:
            url = f"{self.base_url}/api/quote-equity?symbol={symbol}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            return {
                "last_price": data.get("priceInfo", {}).get("lastPrice", 0),
                "high": data.get("priceInfo", {}).get("intraDayHighLow", {}).get("max", 0),
                "low": data.get("priceInfo", {}).get("intraDayHighLow", {}).get("min", 0),
                "open": data.get("priceInfo", {}).get("open", 0),
                "close": data.get("priceInfo", {}).get("close", 0),
                "volume": data.get("priceInfo", {}).get("totalTradedVolume", 0),
                "last_traded_time": data.get("priceInfo", {}).get("lastUpdateTime", "")
            }
        except Exception as e:
            logger.error(f"Error fetching OHLC for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_option_chain(self, symbol: str) -> Dict[str, Any]:
        """Get option chain data for a symbol."""
        try:
            url = f"{self.base_url}/api/option-chain-equities?symbol={symbol}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching option chain for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_technical_indicators(self, symbol: str) -> Dict[str, Any]:
        """Get technical indicators for a symbol."""
        try:
            url = f"{self.base_url}/api/technical-indicators?symbol={symbol}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching technical indicators for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_corporate_info(self, symbol: str) -> Dict[str, Any]:
        """Get corporate information for a symbol."""
        try:
            url = f"{self.base_url}/api/quote-equity?symbol={symbol}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            return {
                "company_name": data.get("info", {}).get("companyName", ""),
                "industry": data.get("info", {}).get("industry", ""),
                "sector": data.get("info", {}).get("sector", ""),
                "isin": data.get("info", {}).get("isin", ""),
                "market_cap": data.get("priceInfo", {}).get("marketCap", 0),
                "face_value": data.get("securityInfo", {}).get("faceValue", 0),
                "book_value": data.get("priceInfo", {}).get("bookValue", 0),
                "dividend_yield": data.get("priceInfo", {}).get("dividendYield", 0)
            }
        except Exception as e:
            logger.error(f"Error fetching corporate info for {symbol}: {str(e)}")
            return None

    def get_all_stocks(self) -> List[str]:
        """Get list of all NSE stocks."""
        try:
            url = f"{self.base_url}/market-data/securities-available-for-trading"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'table'})
            
            stocks = []
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    symbol = cols[1].text.strip()
                    if symbol:
                        stocks.append(f"{symbol}.NS")
            
            return stocks
        except Exception as e:
            logger.error(f"Error fetching all stocks: {str(e)}")
            return []

# Initialize global NSE fetcher instance
nse_fetcher = NSEFetcher() 