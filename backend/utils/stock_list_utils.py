import logging
from functools import lru_cache
from .companies import NSE_COMPANIES, BSE_COMPANIES, NSE_NEXT_50, BSE_100, ALL_COMPANIES

class StockListFetcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @lru_cache(maxsize=1)
    def get_nse_stocks(self):
        try:
            # Return Nifty 50 and Next 50 companies
            return list(set(NSE_COMPANIES + NSE_NEXT_50))
        except Exception as e:
            self.logger.error(f"Error fetching NSE stocks: {str(e)}")
            return []

    @lru_cache(maxsize=1)
    def get_bse_stocks(self):
        try:
            # Return Sensex 30 and BSE 100 companies
            return list(set(BSE_COMPANIES + BSE_100))
        except Exception as e:
            self.logger.error(f"Error fetching BSE stocks: {str(e)}")
            return []

    def get_all_stocks(self):
        try:
            return ALL_COMPANIES
        except Exception as e:
            self.logger.error(f"Error fetching all stocks: {str(e)}")
            return []

# Create a global instance
stock_list_fetcher = StockListFetcher() 