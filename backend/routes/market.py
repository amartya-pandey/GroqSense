from flask import Blueprint, jsonify
import yfinance as yf
from utils.index_list import index_symbols

market_bp = Blueprint("market", __name__)

@market_bp.route("/indices")
def get_indices():
    data = {}
    for name, symbol in index_symbols.items():
        ticker = yf.Ticker(symbol)
        price = ticker.info.get("regularMarketPrice", None)
        data[name] = {
            "symbol": symbol,
            "price": price
        }
    return jsonify(data)
