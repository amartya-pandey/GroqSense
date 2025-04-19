import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, Any
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MoneycontrolFetcher:
    def __init__(self):
        self.base_url = "https://www.moneycontrol.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    @lru_cache(maxsize=1000)
    def get_mini_statement(self, symbol: str) -> Dict[str, Any]:
        """Get mini financial statement for a symbol."""
        try:
            url = f"{self.base_url}/financials/{symbol}/balance-sheetVI"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract key metrics
            metrics = {}
            table = soup.find('table', {'class': 'mctable1'})
            if table:
                for row in table.find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        key = cols[0].text.strip().lower().replace(' ', '_')
                        value = cols[1].text.strip()
                        metrics[key] = self._parse_value(value)
            
            return metrics
        except Exception as e:
            logger.error(f"Error fetching mini statement for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_balance_sheet(self, symbol: str) -> Dict[str, Any]:
        """Get complete balance sheet for a symbol."""
        try:
            url = f"{self.base_url}/financials/{symbol}/balance-sheetVI"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_financial_table(soup)
        except Exception as e:
            logger.error(f"Error fetching balance sheet for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_income_statement(self, symbol: str) -> Dict[str, Any]:
        """Get income statement for a symbol."""
        try:
            url = f"{self.base_url}/financials/{symbol}/profit-lossVI"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_financial_table(soup)
        except Exception as e:
            logger.error(f"Error fetching income statement for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_cash_flow(self, symbol: str) -> Dict[str, Any]:
        """Get cash flow statement for a symbol."""
        try:
            url = f"{self.base_url}/financials/{symbol}/cash-flowVI"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_financial_table(soup)
        except Exception as e:
            logger.error(f"Error fetching cash flow for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_ratios(self, symbol: str) -> Dict[str, Any]:
        """Get key financial ratios for a symbol."""
        try:
            url = f"{self.base_url}/financials/{symbol}/ratiosVI"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_financial_table(soup)
        except Exception as e:
            logger.error(f"Error fetching ratios for {symbol}: {str(e)}")
            return None

    def _parse_financial_table(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Parse financial data table from Moneycontrol."""
        data = {}
        tables = soup.find_all('table', {'class': 'mctable1'})
        
        for table in tables:
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    key = cols[0].text.strip().lower().replace(' ', '_')
                    values = [self._parse_value(col.text.strip()) for col in cols[1:]]
                    data[key] = values if len(values) > 1 else values[0]
        
        return data

    def _parse_value(self, value: str) -> Any:
        """Parse string value to appropriate type."""
        try:
            # Remove commas and convert to float
            value = value.replace(',', '')
            if value.endswith('%'):
                return float(value[:-1])
            return float(value)
        except ValueError:
            return value

# Initialize global Moneycontrol fetcher instance
moneycontrol_fetcher = MoneycontrolFetcher() 