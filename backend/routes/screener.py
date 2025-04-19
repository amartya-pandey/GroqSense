from flask import Blueprint, request, jsonify
from utils.fetch_utils import fetch_financial_ratios

screener_bp = Blueprint("screener", __name__)

@screener_bp.route("/filter", methods=["POST"])
def filter_stocks():
    filters = request.json
    results = fetch_financial_ratios(filters)
    return jsonify(results)
