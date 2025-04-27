from flask import Blueprint, request, jsonify
from backend.utils.pattern_recognition import PatternRecognizer
import pandas as pd
import logging
import os
from dotenv import load_dotenv
# from some_stock_data_service import StockDataService  # Hypothetical service for fetching stock data
import requests

logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

patterns_bp = Blueprint('patterns', __name__)
pattern_recognizer = PatternRecognizer()

@patterns_bp.route('/analyze-trends', methods=['POST'])
def analyze_trends():
    try:
        logging.info("Received request for trend analysis.")
        data = request.json
        logging.info(f"Request data: {data}")
        
        symbol = data.get('symbol')
        period = data.get('period', '1y')
        
        # Directly ask Gemini AI to analyze the trend
        query = f"Analyze trends for {symbol} over {period}."
        summary = pattern_recognizer.analyze_chart(pd.DataFrame(), query)
        logging.info(f"Generated summary: {summary}")
        
        return jsonify({
            'success': True,
            'trend_summary': summary
        })
        
    except Exception as e:
        logging.error(f"Error in analyze_trends: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500