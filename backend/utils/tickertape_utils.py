import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, Any, List
from functools import lru_cache
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TickertapeFetcher:
    def __init__(self):
        self.base_url = "https://api.tickertape.in"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
        }
        self.logger = logging.getLogger(__name__)

    @lru_cache(maxsize=100)
    def get_stock_overview(self, symbol):
        try:
            url = f"{self.base_url}/stocks/{symbol}/overview"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            if not data:
                self.logger.warning(f"No data found for {symbol}")
                return self._get_fallback_data(symbol)
            
            return {
                'name': data.get('name', symbol),
                'sector': data.get('sector', 'Unknown'),
                'industry': data.get('industry', 'Unknown'),
                'description': data.get('description', 'No description available')
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching stock overview for {symbol}: {str(e)}")
            return self._get_fallback_data(symbol)
    
    def _get_fallback_data(self, symbol):
        """Provide fallback data when API calls fail"""
        return {
            'name': symbol,
            'sector': 'Unknown',
            'industry': 'Unknown',
            'description': 'No description available'
        }

    @lru_cache(maxsize=1000)
    def get_technical_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get technical analysis data for a symbol."""
        try:
            url = f"{self.base_url}/stocks/{symbol}/technical"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_technical_data(data)
        except Exception as e:
            logger.error(f"Error fetching technical analysis for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_fundamental_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get fundamental analysis data for a symbol."""
        try:
            url = f"{self.base_url}/stocks/{symbol}/fundamentals"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_fundamental_data(data)
        except Exception as e:
            logger.error(f"Error fetching fundamental analysis for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_peer_comparison(self, symbol: str) -> Dict[str, Any]:
        """Get peer comparison data for a symbol."""
        try:
            url = f"{self.base_url}/stocks/{symbol}/peers"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_peer_data(data)
        except Exception as e:
            logger.error(f"Error fetching peer comparison for {symbol}: {str(e)}")
            return None

    def _parse_overview_data(self, data: Dict) -> Dict[str, Any]:
        """Parse overview data from Tickertape API response."""
        try:
            return {
                "name": data.get("name"),
                "sector": data.get("sector"),
                "industry": data.get("industry"),
                "market_cap": data.get("marketCap"),
                "price": data.get("price"),
                "change_percent": data.get("changePercent"),
                "volume": data.get("volume"),
                "high_52w": data.get("high52w"),
                "low_52w": data.get("low52w"),
                "pe_ratio": data.get("peRatio"),
                "pb_ratio": data.get("pbRatio"),
                "dividend_yield": data.get("dividendYield"),
                "roce": data.get("roce"),
                "roe": data.get("roe"),
                "debt_to_equity": data.get("debtToEquity"),
            }
        except Exception as e:
            logger.error(f"Error parsing overview data: {str(e)}")
            return None

    def _parse_technical_data(self, data: Dict) -> Dict[str, Any]:
        """Parse technical analysis data from Tickertape API response."""
        try:
            return {
                "rsi": data.get("rsi"),
                "macd": data.get("macd"),
                "bollinger_bands": data.get("bollingerBands"),
                "moving_averages": data.get("movingAverages"),
                "support_levels": data.get("supportLevels"),
                "resistance_levels": data.get("resistanceLevels"),
                "trend": data.get("trend"),
                "momentum": data.get("momentum"),
            }
        except Exception as e:
            logger.error(f"Error parsing technical data: {str(e)}")
            return None

    def _parse_fundamental_data(self, data: Dict) -> Dict[str, Any]:
        """Parse fundamental analysis data from Tickertape API response."""
        try:
            return {
                "revenue": data.get("revenue"),
                "profit": data.get("profit"),
                "eps": data.get("eps"),
                "book_value": data.get("bookValue"),
                "cash_flow": data.get("cashFlow"),
                "debt": data.get("debt"),
                "equity": data.get("equity"),
                "operating_margin": data.get("operatingMargin"),
                "net_margin": data.get("netMargin"),
                "return_on_assets": data.get("returnOnAssets"),
                "return_on_equity": data.get("returnOnEquity"),
            }
        except Exception as e:
            logger.error(f"Error parsing fundamental data: {str(e)}")
            return None

    def _parse_peer_data(self, data: Dict) -> Dict[str, Any]:
        """Parse peer comparison data from Tickertape API response."""
        try:
            return {
                "peers": data.get("peers", []),
                "metrics": data.get("metrics", {}),
                "rankings": data.get("rankings", {}),
            }
        except Exception as e:
            logger.error(f"Error parsing peer data: {str(e)}")
            return None

# Initialize global Tickertape fetcher instance
tickertape_fetcher = TickertapeFetcher() 