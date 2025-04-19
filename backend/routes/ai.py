from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/query", methods=["POST"])
def query_ai():
    try:
        data = request.get_json()
        query = data.get("query")
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
            
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({"error": "API key not configured"}), 500

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-saba-24b",
            "messages": [
                {"role": "system", "content": "You are a financial advisor. Provide accurate and helpful financial advice."},
                {"role": "user", "content": query}],
            "temperature": 0.7
        }

        print(f"Sending request to Groq API...")  # Debug log
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions", 
            headers=headers, 
            json=payload
        )
        
        print(f"Groq API response status: {res.status_code}")  # Debug log
        
        if res.status_code != 200:
            print(f"Groq API error: {res.text}")  # Debug log
            return jsonify({"error": f"Groq API Error: {res.text}"}), res.status_code

        json_resp = res.json()
        answer = json_resp["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})

    except Exception as e:
        print(f"Error in query_ai: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500
