import os
from typing import List, Dict, Any
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama2-70b-4096"

class PatternRecognizer:
    def __init__(self):
        pass

    def detect_patterns(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        data_str = data.to_string()
        prompt = f"""
        Analyze the following stock price data and identify any technical patterns:
        {data_str}

        Look for patterns like:
        - Head and Shoulders
        - Double Top/Bottom
        - Triple Top/Bottom
        - Cup and Handle
        - Flags and Pennants
        - Triangles (Ascending/Descending/Symmetrical)

        For each pattern found, provide:
        1. Pattern name
        2. Start and end dates
        3. Confidence level (0-100%)
        4. Potential implications
        """
        return self._call_groq_and_parse_patterns(prompt)

    def analyze_chart(self, data: pd.DataFrame, query: str) -> str:
        data_str = data.to_string()
        prompt = f"""
        Given the following stock price data:
        {data_str}

        Please analyze the chart and answer this query: {query}

        Consider:
        - Technical patterns
        - Support and resistance levels
        - Trend analysis
        - Volume analysis
        - Potential turning points
        """
        return self._call_groq(prompt)

    def _call_groq(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are a financial advisor. Provide accurate and helpful financial advice."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        json_resp = response.json()
        return json_resp["choices"][0]["message"]["content"]

    def _call_groq_and_parse_patterns(self, prompt: str) -> List[Dict[str, Any]]:
        analysis = self._call_groq(prompt)
        return self._parse_patterns(analysis)

    def _parse_patterns(self, analysis: str) -> List[Dict[str, Any]]:
        patterns = []
        lines = analysis.split('\n')
        current_pattern = {}
        for line in lines:
            if 'Pattern:' in line:
                if current_pattern:
                    patterns.append(current_pattern)
                current_pattern = {'name': line.split('Pattern:')[1].strip()}
            elif 'Dates:' in line:
                current_pattern['dates'] = line.split('Dates:')[1].strip()
            elif 'Confidence:' in line:
                current_pattern['confidence'] = float(line.split('Confidence:')[1].strip().replace('%', ''))
            elif 'Implications:' in line:
                current_pattern['implications'] = line.split('Implications:')[1].strip()
        if current_pattern:
            patterns.append(current_pattern)
        return patterns 