import React, { useState } from 'react';
import axios from 'axios';

const Patterns = () => {
    const [symbol, setSymbol] = useState('');
    const [period, setPeriod] = useState('1y');
    const [patterns, setPatterns] = useState(null);
    const [trendSummary, setTrendSummary] = useState('');
    const [error, setError] = useState('');

    const handleAnalyzeTrends = async (event) => {
        event.preventDefault();
        try {
            setError('');
            setPatterns(null);
            setTrendSummary('');

            // Send request to backend
            const response = await axios.post('/patterns/analyze-trends', {
                symbol,
                period
            });

            if (response.data.success) {
                setPatterns(response.data.patterns);
                setTrendSummary(response.data.trend_summary);
            } else {
                setError(response.data.error || 'An error occurred while analyzing trends.');
            }
        } catch (err) {
            setError(err.message || 'Server error.');
        }
    };

    return (
        <div className="patterns-page">
            <h1>Pattern Recognition</h1>
            <form onSubmit={handleAnalyzeTrends}>
                <div>
                    <label>
                        Symbol:
                        <input
                            type="text"
                            value={symbol}
                            onChange={(e) => setSymbol(e.target.value)}
                            placeholder="Enter stock symbol (e.g., SBIN.NS)"
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Period:
                        <select value={period} onChange={(e) => setPeriod(e.target.value)}>
                            <option value="1y">1 Year</option>
                            <option value="6m">6 Months</option>
                            <option value="3m">3 Months</option>
                            <option value="1m">1 Month</option>
                        </select>
                    </label>
                </div>
                <button type="submit">Analyze Trends</button>
            </form>

            {error && <div className="error">Error: {error}</div>}

            {patterns && (
                <div className="patterns">
                    <h2>Detected Patterns</h2>
                    <pre>{JSON.stringify(patterns, null, 2)}</pre>
                </div>
            )}

            {trendSummary && (
                <div className="trend-summary">
                    <h2>Trend Summary</h2>
                    <p>{trendSummary}</p>
                </div>
            )}
        </div>
    );
};

export default Patterns;