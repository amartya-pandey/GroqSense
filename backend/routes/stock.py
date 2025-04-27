from flask import Blueprint, jsonify, request
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/<symbol>')
def get_stock(symbol):
    try:
        # Fetch stock info using yfinance
        stock = yf.Ticker(symbol)
        info = stock.info
        # Extract some common metrics
        metrics = {
            'symbol': symbol,
            'name': info.get('shortName', symbol),
            'exchange': info.get('exchange', ''),
            'price': info.get('regularMarketPrice', 0),
            'pe': info.get('trailingPE', 0),
            'pb': info.get('priceToBook', 0),
            'bookValue': info.get('bookValue', 0),
            'eps': info.get('trailingEps', 0),
            'dividendYield': info.get('dividendYield', 0),
            'roe': info.get('returnOnEquity', 0),
            'marketCap': info.get('marketCap', 0),
            'beta': info.get('beta', 0),
            'avgVolume': info.get('averageVolume', 0),
            'priceToCashFlow': info.get('priceToCashflow', 0),
            'priceToFreeCashFlow': info.get('priceToFreeCashflow', 0)
        }
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/historical/<symbol>')
def get_historical_data(symbol):
    try:
        range_param = request.args.get('range', '1m')
        range_mapping = {
            '5d': ('1d', '5d'),
            '1w': ('1d', '1wk'),
            '1m': ('1d', '1mo'),
            '6m': ('1d', '6mo'),
            '1y': ('1d', '1y'),
            '5y': ('1wk', '5y')
        }
        interval, period = range_mapping.get(range_param, ('1d', '1mo'))

        # Try with .NS and .BSE if not present and if no data is found
        original_symbol = symbol
        stock = yf.Ticker(symbol)
        hist = stock.history(interval=interval, period=period)
        if hist.empty and not symbol.endswith('.NS') and not symbol.endswith('.BSE'):
            test_ns = yf.Ticker(symbol + '.NS').history(interval=interval, period=period)
            if not test_ns.empty:
                symbol = symbol + '.NS'
                hist = test_ns
            else:
                test_bse = yf.Ticker(symbol + '.BSE').history(interval=interval, period=period)
                if not test_bse.empty:
                    symbol = symbol + '.BSE'
                    hist = test_bse

        print(f"YFinance HIST for {symbol}:\n", hist)
        if hist.empty:
            return jsonify({'error': f'No historical data found for symbol {original_symbol}'}), 404

        dates = hist.index.strftime('%Y-%m-%d').tolist()
        prices = hist['Close'].tolist()
        volumes = hist['Volume'].tolist()
        return jsonify({
            'dates': dates,
            'prices': prices,
            'volumes': volumes
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 