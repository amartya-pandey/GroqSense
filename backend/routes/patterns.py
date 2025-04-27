from flask import Blueprint, request, jsonify
from utils.pattern_recognition import PatternRecognizer
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
        historical = data.get('historical')

        # Use the historical data from the frontend if provided
        if historical and 'prices' in historical and 'dates' in historical:
            df = pd.DataFrame({
                'Date': historical['dates'],
                'Close': historical['prices'],
                'Volume': historical['volumes'] if 'volumes' in historical else [None]*len(historical['dates'])
            })
        else:
            df = pd.DataFrame()

        # Use PatternRecognizer to analyze the chart
        summary = pattern_recognizer.analyze_chart(df, f"Analyze trends for {symbol} over {period}.")
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
