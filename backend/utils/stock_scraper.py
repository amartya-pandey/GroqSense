import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from typing import List, Dict, Tuple
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_nse_stocks() -> List[str]:
    """
    Scrape all NSE-listed stocks from the NSE website.
    Returns a list of stock symbols with .NS suffix.
    """
    try:
        # NSE URL for equity list
        url = "https://www.nseindia.com/market-data/securities-available-for-trading"
        
        # Headers to mimic browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing stock data
        table = soup.find('table', {'class': 'table'})
        if not table:
            logger.error("Could not find stock table in NSE website")
            return []
        
        # Extract stock symbols
        stocks = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 2:
                symbol = cols[1].text.strip()
                if symbol:
                    stocks.append(f"{symbol}.NS")
        
        logger.info(f"Successfully scraped {len(stocks)} stocks from NSE")
        return stocks
        
    except Exception as e:
        logger.error(f"Error scraping NSE stocks: {str(e)}")
        return []

def get_bse_stocks() -> List[str]:
    """
    Scrape all BSE-listed stocks from the BSE website.
    Returns a list of stock symbols with .BO suffix.
    """
    try:
        # BSE URL for equity list
        url = "https://www.bseindia.com/corporates/List_Scrips.html"
        
        # Headers to mimic browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing stock data
        table = soup.find('table', {'class': 'table'})
        if not table:
            logger.error("Could not find stock table in BSE website")
            return []
        
        # Extract stock symbols
        stocks = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 2:
                symbol = cols[1].text.strip()
                if symbol:
                    stocks.append(f"{symbol}.BO")
        
        logger.info(f"Successfully scraped {len(stocks)} stocks from BSE")
        return stocks
        
    except Exception as e:
        logger.error(f"Error scraping BSE stocks: {str(e)}")
        return []

def get_stock_sectors(exchange: str) -> Dict[str, str]:
    """
    Get sector information for stocks from NSE/BSE website.
    Returns a dictionary mapping stock symbols to their sectors.
    """
    try:
        if exchange == "NSE":
            url = "https://www.nseindia.com/market-data/securities-available-for-trading"
        else:
            url = "https://www.bseindia.com/corporates/List_Scrips.html"
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'table'})
        
        sectors = {}
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 3:
                symbol = cols[1].text.strip()
                sector = cols[2].text.strip()
                if symbol and sector:
                    suffix = ".NS" if exchange == "NSE" else ".BO"
                    sectors[f"{symbol}{suffix}"] = sector
        
        return sectors
        
    except Exception as e:
        logger.error(f"Error getting stock sectors for {exchange}: {str(e)}")
        return {}

def get_all_stocks_with_sectors() -> Dict[str, Dict[str, str]]:
    """
    Get all NSE and BSE stocks with their sector information.
    Returns a dictionary with stock symbols as keys and their details as values.
    """
    # Get NSE stocks
    nse_stocks = get_nse_stocks()
    nse_sectors = get_stock_sectors("NSE")
    
    # Get BSE stocks
    bse_stocks = get_bse_stocks()
    bse_sectors = get_stock_sectors("BSE")
    
    result = {}
    
    # Process NSE stocks
    for stock in nse_stocks:
        result[stock] = {
            "sector": nse_sectors.get(stock, "Unknown"),
            "exchange": "NSE",
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Process BSE stocks
    for stock in bse_stocks:
        result[stock] = {
            "sector": bse_sectors.get(stock, "Unknown"),
            "exchange": "BSE",
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Save to file for debugging
    with open("stock_data.json", "w") as f:
        json.dump(result, f, indent=2)
    
    return result 