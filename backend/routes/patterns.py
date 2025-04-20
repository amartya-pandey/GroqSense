from flask import Blueprint, request, jsonify
from backend.utils.pattern_recognition import PatternRecognizer
import yfinance as yf
import pandas as pd

patterns_bp = Blueprint('patterns', __name__)
pattern_recognizer = PatternRecognizer()

@patterns_bp.route('/detect-patterns', methods=['POST'])
def detect_patterns():
    try:
        data = request.json
        symbol = data.get('symbol')
        period = data.get('period', '1y')
        
        # Fetch stock data
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        
        # Detect patterns
        patterns = pattern_recognizer.detect_patterns(df)
        
        return jsonify({
            'success': True,
            'patterns': patterns
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patterns_bp.route('/analyze-chart', methods=['POST'])
def analyze_chart():
    try:
        data = request.json
        symbol = data.get('symbol')
        query = data.get('query')
        period = data.get('period', '1y')
        
        # Fetch stock data
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        
        # Analyze chart based on query
        analysis = pattern_recognizer.analyze_chart(df, query)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 