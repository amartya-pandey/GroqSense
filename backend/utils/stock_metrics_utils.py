import yfinance as yf
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockMetricsFetcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @lru_cache(maxsize=100)
    def get_stock_metrics(self, symbol):
        try:
            # Add .NS suffix for NSE stocks
            ticker = yf.Ticker(f"{symbol}.NS")
            
            # Get basic info
            info = ticker.info
            if not info:
                self.logger.warning(f"No info found for {symbol}")
                return self._get_fallback_data(symbol)
            
            # Extract metrics
            metrics = {
                'price': info.get('regularMarketPrice', 0),
                'pe': info.get('trailingPE', 0),
                'pb': info.get('priceToBook', 0),
                'bookValue': info.get('bookValue', 0),
                'eps': info.get('trailingEps', 0),
                'dividendYield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                'cagr5Y': info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0,
                'debtToEquity': info.get('debtToEquity', 0),
                'marketCap': info.get('marketCap', 0) / 1e7,  # Convert to crores
                'beta': info.get('beta', 0),
                'avgVolume': info.get('averageVolume', 0)
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error fetching stock metrics for {symbol}: {str(e)}")
            return self._get_fallback_data(symbol)
    
    def _get_fallback_data(self, symbol):
        """Provide fallback data when API calls fail"""
        return {
            'price': 0,
            'pe': 0,
            'pb': 0,
            'bookValue': 0,
            'eps': 0,
            'dividendYield': 0,
            'roe': 0,
            'cagr5Y': 0,
            'debtToEquity': 0,
            'marketCap': 0,
            'beta': 0,
            'avgVolume': 0
        }

# Create a global instance
stock_metrics_fetcher = StockMetricsFetcher() 