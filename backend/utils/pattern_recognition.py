import os
from typing import List, Dict, Any
import pandas as pd
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GeminiAPI_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash-latest')

class PatternRecognizer:
    def __init__(self):
        self.chat = model.start_chat()
        
    def detect_patterns(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect technical patterns in the given price data using Gemini's LLM.
        
        Args:
            data (pd.DataFrame): DataFrame containing OHLCV data
            
        Returns:
            List[Dict[str, Any]]: List of detected patterns with their details
        """
        # Convert data to a format suitable for LLM analysis
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
        
        response = self.chat.send_message(prompt)
        
        return self._parse_patterns(response.text)
    
    def analyze_chart(self, data: pd.DataFrame, query: str) -> str:
        """
        Analyze the chart based on a natural language query.
        
        Args:
            data (pd.DataFrame): DataFrame containing OHLCV data
            query (str): Natural language query about the chart
            
        Returns:
            str: AI-generated analysis
        """
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
        
        response = self.chat.send_message(prompt)
        
        return response.text
    
    def _parse_patterns(self, analysis: str) -> List[Dict[str, Any]]:
        """
        Parse the LLM's pattern analysis into a structured format.
        
        Args:
            analysis (str): Raw analysis text from LLM
            
        Returns:
            List[Dict[str, Any]]: Structured pattern data
        """
        # This is a simplified parser - you may want to enhance it based on your needs
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