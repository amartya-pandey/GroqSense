from flask import Blueprint, request, jsonify
from utils.stock_metrics_utils import stock_metrics_fetcher
from utils.tickertape_utils import tickertape_fetcher
from utils.stock_list_utils import stock_list_fetcher
from utils.companies import NSE_COMPANIES, BSE_COMPANIES, NSE_NEXT_50, BSE_100
import logging

screener_bp = Blueprint('screener', __name__)

import redis
import json
import time

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Define which metrics should use <= for filtering
LOWER_BOUND_METRICS = {
    'pe', 'pb', 'debtToEquity', 'beta', 'priceToCashFlow', 'priceToFreeCashFlow'
}

@screener_bp.route('/filter', methods=['POST'])
def filter_stocks():
    try:
        data = request.get_json() or {}
        filters = data.get('filters', {})
        exchange = data.get('exchange', 'both')  # 'nse', 'bse', or 'both'
        index = data.get('index', 'all')  # 'all', 'nifty50', 'niftynext50', 'sensex30', 'bse100'
        
        logging.info(f"Received screener filters: {filters}, exchange: {exchange}, index: {index}")
        
        # Get stocks based on exchange and index
        if index == 'nifty50':
            stocks = NSE_COMPANIES
        elif index == 'niftynext50':
            stocks = NSE_NEXT_50
        elif index == 'sensex30':
            stocks = BSE_COMPANIES
        elif index == 'bse100':
            stocks = BSE_100
        else:
            if exchange == 'nse':
                stocks = stock_list_fetcher.get_nse_stocks()
            elif exchange == 'bse':
                stocks = stock_list_fetcher.get_bse_stocks()
            else:
                stocks = stock_list_fetcher.get_all_stocks()
        
        results = []
        
        for symbol in stocks:
            try:
                # Check if data is cached in Redis
                cache_key = f"stock_data:{symbol}"
                cached_data = redis_client.get(cache_key)
                
                if cached_data:
                    # Use cached data
                    stock_data = json.loads(cached_data)
                    logging.info(f"Cache hit for {symbol}")
                else:
                    # Fetch data if not in cache
                    logging.info(f"Cache miss for {symbol}. Fetching data from web.")
                    metrics = stock_metrics_fetcher.get_stock_metrics(symbol)
                    if not metrics:
                        logging.warning(f"No metrics found for {symbol}")
                        continue
                    
                    tickertape_data = tickertape_fetcher.get_stock_overview(symbol)
                    
                    # Combine data
                    stock_data = {
                        'symbol': symbol,
                        'name': tickertape_data.get('name', symbol),
                        'exchange': 'NSE' if symbol in stock_list_fetcher.get_nse_stocks() else 'BSE',
                        'price': metrics.get('price', 0),
                        'pe': metrics.get('pe', 0),
                        'pb': metrics.get('pb', 0),
                        'bookValue': metrics.get('bookValue', 0),
                        'eps': metrics.get('eps', 0),
                        'dividendYield': metrics.get('dividendYield', 0),
                        'roe': metrics.get('roe', 0),
                        'cagr5Y': metrics.get('cagr5Y', 0),
                        'debtToEquity': metrics.get('debtToEquity', 0),
                        'marketCap': metrics.get('marketCap', 0),
                        'beta': metrics.get('beta', 0),
                        'avgVolume': metrics.get('avgVolume', 0),
                        'cashPerShare': metrics.get('cashPerShare', 0),
                        'priceToCashFlow': metrics.get('priceToCashFlow', 0),
                        'priceToFreeCashFlow': metrics.get('priceToFreeCashFlow', 0)
                    }
                    
                    # Cache the data in Redis (set expiration time to 18 hours)
                    redis_client.set(cache_key, json.dumps(stock_data), ex=64800)
                    logging.info(f"Data for {symbol} cached for 18 hours.")
                
                # Apply filters
                if all(
                    not filters.get(key) or 
                    (isinstance(stock_data.get(key), (int, float)) and 
                    (stock_data[key] <= float(filters[key]) if key in LOWER_BOUND_METRICS 
                    else stock_data[key] >= float(filters[key])))
                    for key in filters
                ):
                    results.append(stock_data)
                    
            except Exception as e:
                logging.error(f"Error processing stock {symbol}: {str(e)}")
                continue

        return jsonify(results)
        
    except Exception as e:
        logging.error(f"Error in filter_stocks: {str(e)}")
        return jsonify([]), 500

@screener_bp.route('/get-stock-data', methods=['POST'])
def get_stock_data():
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        period = data.get('period', '1y')
        
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
        
        # Fetch stock data using stock_metrics_fetcher
        metrics = stock_metrics_fetcher.get_stock_metrics(symbol)
        if not metrics:
            return jsonify({'error': 'Failed to fetch stock metrics'}), 500
        
        # Fetch additional data from tickertape
        tickertape_data = tickertape_fetcher.get_stock_overview(symbol)
        if not tickertape_data:
            return jsonify({'error': 'Failed to fetch tickertape data'}), 500
        
        # Combine data
        stock_data = {
            'symbol': symbol,
            'name': tickertape_data.get('name', symbol),
            'exchange': 'NSE' if symbol in stock_list_fetcher.get_nse_stocks() else 'BSE',
            'price': metrics.get('price', 0),
            'pe': metrics.get('pe', 0),
            'pb': metrics.get('pb', 0),
            'bookValue': metrics.get('bookValue', 0),
            'eps': metrics.get('eps', 0),
            'dividendYield': metrics.get('dividendYield', 0),
            'roe': metrics.get('roe', 0),
            'cagr5Y': metrics.get('cagr5Y', 0),
            'debtToEquity': metrics.get('debtToEquity', 0),
            'marketCap': metrics.get('marketCap', 0),
            'beta': metrics.get('beta', 0),
            'avgVolume': metrics.get('avgVolume', 0),
            'cashPerShare': metrics.get('cashPerShare', 0),
            'priceToCashFlow': metrics.get('priceToCashFlow', 0),
            'priceToFreeCashFlow': metrics.get('priceToFreeCashFlow', 0)
        }
        
        return jsonify(stock_data)
    except Exception as e:
        logging.error(f"Error in get_stock_data: {str(e)}")
        return jsonify({'error': str(e)}), 500