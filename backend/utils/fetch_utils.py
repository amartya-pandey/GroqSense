import yfinance as yf
import pandas as pd
from typing import Dict, List, Any
import logging
import time
from functools import lru_cache
from .stock_scraper import get_all_stocks_with_sectors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache stock data for 1 hour
@lru_cache(maxsize=1)
def get_cached_stocks():
    """Get cached list of all NSE and BSE stocks with sectors."""
    return get_all_stocks_with_sectors()

@lru_cache(maxsize=1000, ttl=3600)  # Cache 1000 stocks for 1 hour
# @lru_cache(maxsize=1000,)  # Cache 1000 stocks for 1 hour
def get_stock_info(ticker: str) -> Dict[str, Any]:
    """Fetch detailed financial information for a given stock ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get stock details from cache
        stock_details = get_cached_stocks().get(ticker, {})
        
        # Extract relevant metrics
        return {
            "symbol": ticker,
            "name": info.get("longName", ""),
            "sector": stock_details.get("sector", "Unknown"),
            "exchange": stock_details.get("exchange", "Unknown"),
            
            # Valuation Metrics
            "pe": info.get("trailingPE", 0),
            "pb": info.get("priceToBook", 0),
            "ps": info.get("priceToSalesTrailing12Months", 0),
            "peg": info.get("pegRatio", 0),
            "enterpriseValue": info.get("enterpriseValue", 0) / 10000000,  # Convert to Crores
            "enterpriseToEbitda": info.get("enterpriseToEbitda", 0),
            
            # Profitability Metrics
            "roe": info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0,
            "roce": info.get("returnOnCapitalEmployed", 0) * 100 if info.get("returnOnCapitalEmployed") else 0,
            "roa": info.get("returnOnAssets", 0) * 100 if info.get("returnOnAssets") else 0,
            "operatingMargin": info.get("operatingMargins", 0) * 100 if info.get("operatingMargins") else 0,
            "profitMargin": info.get("profitMargins", 0) * 100 if info.get("profitMargins") else 0,
            
            # Growth Metrics
            "revenueGrowth": info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0,
            "earningsGrowth": info.get("earningsGrowth", 0) * 100 if info.get("earningsGrowth") else 0,
            "cagr5Y": info.get("earningsGrowth", 0) * 100 if info.get("earningsGrowth") else 0,
            
            # Financial Health
            "marketCap": info.get("marketCap", 0) / 10000000,  # Convert to Crores
            "debtToEquity": info.get("debtToEquity", 0),
            "currentRatio": info.get("currentRatio", 0),
            "quickRatio": info.get("quickRatio", 0),
            "interestCoverage": info.get("interestCoverage", 0),
            
            # Dividend Metrics
            "dividendYield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
            "payoutRatio": info.get("payoutRatio", 0) * 100 if info.get("payoutRatio") else 0,
            "dividendGrowth": info.get("dividendGrowth", 0) * 100 if info.get("dividendGrowth") else 0,
            
            # Per Share Metrics
            "eps": info.get("trailingEps", 0),
            "bookValuePerShare": info.get("bookValue", 0),
            "cashPerShare": info.get("totalCashPerShare", 0),
            
            # Price Information
            "price": info.get("regularMarketPrice", 0),
            "priceToCashFlow": info.get("priceToCashFlow", 0),
            "priceToFreeCashFlow": info.get("priceToFreeCashFlow", 0),
            
            # Volume and Liquidity
            "avgVolume": info.get("averageVolume", 0),
            "volume": info.get("regularMarketVolume", 0),
            "beta": info.get("beta", 0),
            
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def meets_criteria(stock_data: Dict[str, Any], filters: Dict[str, float]) -> bool:
    """Check if a stock meets all the specified filter criteria."""
    try:
        # Exchange filter
        if filters.get("exchange") and stock_data["exchange"] != filters["exchange"]:
            return False
            
        # Valuation Metrics
        if filters.get("pe") and stock_data["pe"] > filters["pe"]:
            return False
        if filters.get("pb") and stock_data["pb"] > filters["pb"]:
            return False
        if filters.get("ps") and stock_data["ps"] > filters["ps"]:
            return False
        if filters.get("peg") and stock_data["peg"] > filters["peg"]:
            return False
        if filters.get("enterpriseToEbitda") and stock_data["enterpriseToEbitda"] > filters["enterpriseToEbitda"]:
            return False
            
        # Profitability Metrics
        if filters.get("roe") and stock_data["roe"] < filters["roe"]:
            return False
        if filters.get("roce") and stock_data["roce"] < filters["roce"]:
            return False
        if filters.get("roa") and stock_data["roa"] < filters["roa"]:
            return False
        if filters.get("operatingMargin") and stock_data["operatingMargin"] < filters["operatingMargin"]:
            return False
        if filters.get("profitMargin") and stock_data["profitMargin"] < filters["profitMargin"]:
            return False
            
        # Growth Metrics
        if filters.get("revenueGrowth") and stock_data["revenueGrowth"] < filters["revenueGrowth"]:
            return False
        if filters.get("earningsGrowth") and stock_data["earningsGrowth"] < filters["earningsGrowth"]:
            return False
        if filters.get("cagr5Y") and stock_data["cagr5Y"] < filters["cagr5Y"]:
            return False
            
        # Financial Health
        if filters.get("marketCap") and stock_data["marketCap"] < filters["marketCap"]:
            return False
        if filters.get("debtToEquity") and stock_data["debtToEquity"] > filters["debtToEquity"]:
            return False
        if filters.get("currentRatio") and stock_data["currentRatio"] < filters["currentRatio"]:
            return False
        if filters.get("quickRatio") and stock_data["quickRatio"] < filters["quickRatio"]:
            return False
        if filters.get("interestCoverage") and stock_data["interestCoverage"] < filters["interestCoverage"]:
            return False
            
        # Dividend Metrics
        if filters.get("dividendYield") and stock_data["dividendYield"] < filters["dividendYield"]:
            return False
        if filters.get("payoutRatio") and stock_data["payoutRatio"] > filters["payoutRatio"]:
            return False
        if filters.get("dividendGrowth") and stock_data["dividendGrowth"] < filters["dividendGrowth"]:
            return False
            
        # Per Share Metrics
        if filters.get("eps") and stock_data["eps"] < filters["eps"]:
            return False
        if filters.get("bookValuePerShare") and stock_data["bookValuePerShare"] < filters["bookValuePerShare"]:
            return False
        if filters.get("cashPerShare") and stock_data["cashPerShare"] < filters["cashPerShare"]:
            return False
            
        # Price Information
        if filters.get("priceToCashFlow") and stock_data["priceToCashFlow"] > filters["priceToCashFlow"]:
            return False
        if filters.get("priceToFreeCashFlow") and stock_data["priceToFreeCashFlow"] > filters["priceToFreeCashFlow"]:
            return False
            
        # Volume and Liquidity
        if filters.get("avgVolume") and stock_data["avgVolume"] < filters["avgVolume"]:
            return False
        if filters.get("beta") and stock_data["beta"] > filters["beta"]:
            return False
            
        return True
    except Exception as e:
        logger.error(f"Error checking criteria for {stock_data.get('symbol')}: {str(e)}")
        return False

def fetch_financial_ratios(filters: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Fetch and filter stocks based on the provided criteria.
    
    Args:
        filters: Dictionary containing filter criteria
        
    Returns:
        List of stocks that meet the criteria
    """
    try:
        # Get all stocks from cache
        all_stocks = list(get_cached_stocks().keys())
        logger.info(f"Processing {len(all_stocks)} stocks")
        
        results = []
        for ticker in all_stocks:
            stock_data = get_stock_info(ticker)
            if stock_data and meets_criteria(stock_data, filters):
                results.append(stock_data)
                
        # Sort results by market cap (descending)
        results.sort(key=lambda x: x["marketCap"], reverse=True)
        
        logger.info(f"Found {len(results)} stocks matching criteria")
        return results
    except Exception as e:
        logger.error(f"Error in fetch_financial_ratios: {str(e)}")
        return []
