import React, { useState } from 'react';
import { patternApi } from '../api/patternApi';
import '../styles/PatternRecognition.css';

const PatternRecognition = () => {
    const [symbol, setSymbol] = useState('');
    const [period, setPeriod] = useState('1y');
    const [query, setQuery] = useState('');
    const [patterns, setPatterns] = useState([]);
    const [analysis, setAnalysis] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const formatConfidence = (confidence) => {
        if (typeof confidence === 'number') {
            return `${confidence.toFixed(1)}%`;
        }
        return 'N/A';
    };

    const formatDates = (dates) => {
        if (!dates) return 'N/A';
        if (typeof dates === 'string') return dates;
        if (dates.start && dates.end) {
            return `${dates.start} to ${dates.end}`;
        }
        return 'N/A';
    };

    const handleDetectPatterns = async () => {
        try {
            setLoading(true);
            setError('');
            const response = await patternApi.detectPatterns(symbol, period);
            if (response.success && response.patterns) {
                const validPatterns = response.patterns.filter(pattern => 
                    pattern && typeof pattern === 'object'
                );
                setPatterns(validPatterns);
                if (validPatterns.length === 0) {
                    setError('No clear patterns detected in the current timeframe');
                }
            } else {
                setError(response.error || 'Failed to detect patterns');
            }
        } catch (err) {
            setError('An error occurred while detecting patterns');
        } finally {
            setLoading(false);
        }
    };

    const handleAnalyzeChart = async () => {
        try {
            setLoading(true);
            setError('');
            const response = await patternApi.analyzeChart(symbol, query, period);
            if (response.success) {
                setAnalysis(response.analysis);
            } else {
                setError(response.error || 'Failed to analyze chart');
            }
        } catch (err) {
            setError('An error occurred while analyzing the chart');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="pattern-recognition">
            <h2>Pattern Recognition</h2>
            
            <div className="input-group">
                <input
                    type="text"
                    placeholder="Enter stock symbol (e.g., RELIANCE.NS)"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value)}
                />
                <select value={period} onChange={(e) => setPeriod(e.target.value)}>
                    <option value="1d">1 Day</option>
                    <option value="5d">5 Days</option>
                    <option value="1mo">1 Month</option>
                    <option value="3mo">3 Months</option>
                    <option value="6mo">6 Months</option>
                    <option value="1y">1 Year</option>
                    <option value="2y">2 Years</option>
                    <option value="5y">5 Years</option>
                </select>
            </div>

            <div className="button-group">
                <button onClick={handleDetectPatterns} disabled={loading || !symbol}>
                    {loading ? 'Detecting...' : 'Detect Patterns'}
                </button>
            </div>

            {patterns.length > 0 && (
                <div className="patterns-list">
                    <h3>Detected Patterns</h3>
                    {patterns.map((pattern, index) => (
                        <div key={index} className="pattern-card">
                            <h4>{pattern.name || 'Unknown Pattern Type'}</h4>
                            <p><strong>Dates:</strong> {formatDates(pattern.dates)}</p>
                            <p><strong>Confidence:</strong> {formatConfidence(pattern.confidence)}</p>
                            <p><strong>Implications:</strong> {pattern.implications || 'Analysis not available'}</p>
                        </div>
                    ))}
                </div>
            )}

            <div className="analysis-section">
                <h3>Ask About the Chart</h3>
                <input
                    type="text"
                    placeholder="Enter your question (e.g., Show me bullish patterns)"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button onClick={handleAnalyzeChart} disabled={loading || !symbol || !query}>
                    {loading ? 'Analyzing...' : 'Analyze Chart'}
                </button>

                {analysis && (
                    <div className="analysis-result">
                        <h4>Analysis Result</h4>
                        <p>{analysis}</p>
                    </div>
                )}
            </div>

            {error && <div className="error-message">{error}</div>}
            {loading && <div className="loading">Processing chart data...</div>}
        </div>
    );
};

export default PatternRecognition; 