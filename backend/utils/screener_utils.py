import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, Any, List
from functools import lru_cache
import json
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScreenerFetcher:
    def __init__(self):
        self.base_url = "https://www.screener.in"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    @lru_cache(maxsize=1000)
    def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """Get company information from Screener.in."""
        try:
            url = f"{self.base_url}/company/{symbol}/"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_company_info(soup)
        except Exception as e:
            logger.error(f"Error fetching company info for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_financial_ratios(self, symbol: str) -> Dict[str, Any]:
        """Get financial ratios from Screener.in."""
        try:
            url = f"{self.base_url}/company/{symbol}/ratios/"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_financial_ratios(soup)
        except Exception as e:
            logger.error(f"Error fetching financial ratios for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_quarterly_results(self, symbol: str) -> Dict[str, Any]:
        """Get quarterly results from Screener.in."""
        try:
            url = f"{self.base_url}/company/{symbol}/consolidated/"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_quarterly_results(soup)
        except Exception as e:
            logger.error(f"Error fetching quarterly results for {symbol}: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def get_shareholding(self, symbol: str) -> Dict[str, Any]:
        """Get shareholding pattern from Screener.in."""
        try:
            url = f"{self.base_url}/company/{symbol}/shareholding/"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_shareholding(soup)
        except Exception as e:
            logger.error(f"Error fetching shareholding for {symbol}: {str(e)}")
            return None

    def _parse_company_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Parse company information from Screener.in HTML."""
        try:
            info = {}
            
            # Get company name and sector
            header = soup.find('div', class_='company-header')
            if header:
                info['name'] = header.find('h1').text.strip()
                info['sector'] = header.find('a', class_='sector').text.strip()
            
            # Get key metrics
            metrics = soup.find('div', class_='company-ratios')
            if metrics:
                for metric in metrics.find_all('li'):
                    key = metric.find('span', class_='name').text.strip()
                    value = metric.find('span', class_='value').text.strip()
                    info[key.lower().replace(' ', '_')] = value
            
            return info
        except Exception as e:
            logger.error(f"Error parsing company info: {str(e)}")
            return None

    def _parse_financial_ratios(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Parse financial ratios from Screener.in HTML."""
        try:
            ratios = {}
            
            # Get ratio tables
            tables = soup.find_all('table', class_='data-table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header row
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        ratio_name = cols[0].text.strip()
                        ratio_value = cols[1].text.strip()
                        ratios[ratio_name.lower().replace(' ', '_')] = ratio_value
            
            return ratios
        except Exception as e:
            logger.error(f"Error parsing financial ratios: {str(e)}")
            return None

    def _parse_quarterly_results(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Parse quarterly results from Screener.in HTML."""
        try:
            results = {}
            
            # Get quarterly results table
            table = soup.find('table', class_='data-table')
            if table:
                headers = [th.text.strip() for th in table.find_all('th')]
                rows = table.find_all('tr')
                
                for row in rows[1:]:  # Skip header row
                    cols = row.find_all('td')
                    if len(cols) == len(headers):
                        quarter = cols[0].text.strip()
                        quarter_data = {}
                        for i in range(1, len(headers)):
                            quarter_data[headers[i].lower().replace(' ', '_')] = cols[i].text.strip()
                        results[quarter] = quarter_data
            
            return results
        except Exception as e:
            logger.error(f"Error parsing quarterly results: {str(e)}")
            return None

    def _parse_shareholding(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Parse shareholding pattern from Screener.in HTML."""
        try:
            shareholding = {}
            
            # Get shareholding tables
            tables = soup.find_all('table', class_='data-table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header row
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        holder = cols[0].text.strip()
                        percentage = cols[1].text.strip()
                        shareholding[holder.lower().replace(' ', '_')] = percentage
            
            return shareholding
        except Exception as e:
            logger.error(f"Error parsing shareholding: {str(e)}")
            return None

# Initialize global Screener fetcher instance
screener_fetcher = ScreenerFetcher() 