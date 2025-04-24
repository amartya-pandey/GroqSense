from flask import Blueprint, jsonify, request
from ..utils.alpha_vantage_stock import AlphaVantageStock
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

stock_bp = Blueprint('stock', __name__)
stock_analyzer = AlphaVantageStock()

@stock_bp.route('/<symbol>')
def get_stock(symbol):
    try:
        metrics = stock_analyzer.get_stock_metrics(symbol)
        yf_data = stock_analyzer.get_yfinance_supplement(symbol)
        combined_data = {**metrics, **yf_data}
        return jsonify(combined_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/historical/<symbol>')
def get_historical_data(symbol):
    try:
        range_param = request.args.get('range', '1m')
        
        # Map range parameter to yfinance interval and period
        range_mapping = {
            '5d': ('1d', '5d'),
            '1w': ('1d', '1wk'),
            '1m': ('1d', '1mo'),
            '6m': ('1d', '6mo'),
            '1y': ('1d', '1y'),
            '5y': ('1wk', '5y')
        }
        
        interval, period = range_mapping.get(range_param, ('1d', '1mo'))
        
        # Fetch historical data using yfinance
        stock = yf.Ticker(symbol)
        hist = stock.history(interval=interval, period=period)
        
        # Calculate moving averages
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        
        # Format data for chart
        dates = hist.index.strftime('%Y-%m-%d').tolist()
        prices = hist['Close'].tolist()
        volumes = hist['Volume'].tolist()
        ma20 = hist['MA20'].tolist()
        ma50 = hist['MA50'].tolist()
        
        return jsonify({
            'dates': dates,
            'prices': prices,
            'volumes': volumes,
            'ma20': ma20,
            'ma50': ma50
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 