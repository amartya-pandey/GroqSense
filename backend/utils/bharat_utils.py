from Bharat_sm_data import NSE, Moneycontrol, Tickertape
import logging
from typing import Dict, Any
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
nse = NSE()
moneycontrol = Moneycontrol()
tickertape = Tickertape()

@lru_cache(maxsize=1000)
def get_bharat_stock_info(symbol: str) -> Dict[str, Any]:
    """Get comprehensive stock information using Bharat-SM-Data."""
    try:
        # Get basic info from NSE
        nse_info = nse.get_ohlc(symbol)
        
        # Get fundamental data from Moneycontrol
        mc_info = moneycontrol.get_mini_statement(symbol)
        
        # Get additional metrics from Tickertape
        tt_info = tickertape.get_key_ratios(symbol)
        
        # Combine all data
        return {
            "symbol": symbol,
            "price": nse_info.get("last_price", 0),
            "high": nse_info.get("high", 0),
            "low": nse_info.get("low", 0),
            "volume": nse_info.get("volume", 0),
            
            # Valuation Metrics
            "pe": tt_info.get("pe_ratio", 0),
            "pb": tt_info.get("pb_ratio", 0),
            "ps": tt_info.get("ps_ratio", 0),
            "peg": tt_info.get("peg_ratio", 0),
            
            # Profitability Metrics
            "roe": mc_info.get("return_on_equity", 0),
            "roce": mc_info.get("return_on_capital_employed", 0),
            "roa": mc_info.get("return_on_assets", 0),
            "operatingMargin": mc_info.get("operating_margin", 0),
            "profitMargin": mc_info.get("net_profit_margin", 0),
            
            # Growth Metrics
            "revenueGrowth": mc_info.get("revenue_growth", 0),
            "earningsGrowth": mc_info.get("earnings_growth", 0),
            
            # Financial Health
            "debtToEquity": mc_info.get("debt_to_equity", 0),
            "currentRatio": mc_info.get("current_ratio", 0),
            "quickRatio": mc_info.get("quick_ratio", 0),
            
            # Dividend Metrics
            "dividendYield": tt_info.get("dividend_yield", 0),
            "payoutRatio": tt_info.get("payout_ratio", 0),
            
            # Additional Metrics
            "marketCap": mc_info.get("market_cap", 0),
            "enterpriseValue": mc_info.get("enterprise_value", 0),
            "beta": tt_info.get("beta", 0),
            
            "last_updated": nse_info.get("last_traded_time", "")
        }
    except Exception as e:
        logger.error(f"Error fetching Bharat-SM-Data for {symbol}: {str(e)}")
        return None

def get_option_chain(symbol: str) -> Dict[str, Any]:
    """Get option chain data for a symbol."""
    try:
        return nse.get_option_chain(symbol)
    except Exception as e:
        logger.error(f"Error fetching option chain for {symbol}: {str(e)}")
        return None

def get_technical_indicators(symbol: str) -> Dict[str, Any]:
    """Get technical indicators for a symbol."""
    try:
        return nse.get_technical_indicators(symbol)
    except Exception as e:
        logger.error(f"Error fetching technical indicators for {symbol}: {str(e)}")
        return None

def get_fundamental_analysis(symbol: str) -> Dict[str, Any]:
    """Get comprehensive fundamental analysis."""
    try:
        # Get financial statements
        balance_sheet = moneycontrol.get_balance_sheet(symbol)
        income_statement = moneycontrol.get_income_statement(symbol)
        cash_flow = moneycontrol.get_cash_flow(symbol)
        
        # Get ratios and metrics
        ratios = moneycontrol.get_ratios(symbol)
        peer_comparison = tickertape.get_peer_comparison(symbol)
        
        return {
            "balance_sheet": balance_sheet,
            "income_statement": income_statement,
            "cash_flow": cash_flow,
            "ratios": ratios,
            "peer_comparison": peer_comparison
        }
    except Exception as e:
        logger.error(f"Error fetching fundamental analysis for {symbol}: {str(e)}")
        return None 