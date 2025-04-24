import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import StockGraph from '../components/StockGraph';

const StockDetail = () => {
    const { symbol } = useParams();
    const navigate = useNavigate();
    const [stockData, setStockData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStockData = async () => {
            try {
                setLoading(true);
                const response = await axios.get(`/api/stock/${symbol}`);
                setStockData(response.data);
            } catch (error) {
                console.error('Error fetching stock data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStockData();
    }, [symbol]);

    if (loading) {
        return <div className="loading">Loading stock data...</div>;
    }

    if (!stockData) {
        return <div className="error">Error loading stock data</div>;
    }

    const metricGroups = {
        'Valuation': [
            { key: 'Current Price', format: (v) => `$${v?.toFixed(2) || 'N/A'}` },
            { key: 'Market Cap (B)', format: (v) => `$${v?.toFixed(2)}B` },
            { key: 'P/E Ratio', format: (v) => v?.toFixed(2) || 'N/A' },
            { key: 'Forward P/E', format: (v) => v?.toFixed(2) || 'N/A' },
            { key: 'P/B Ratio', format: (v) => v?.toFixed(2) || 'N/A' },
            { key: 'P/S Ratio', format: (v) => v?.toFixed(2) || 'N/A' },
            { key: 'Enterprise Value (B)', format: (v) => `$${v?.toFixed(2)}B` },
            { key: 'Enterprise Value/EBITDA', format: (v) => v?.toFixed(2) || 'N/A' }
        ],
        'Growth & Profitability': [
            { key: 'ROE (%)', format: (v) => `${v?.toFixed(2)}%` },
            { key: 'ROA (%)', format: (v) => `${v?.toFixed(2)}%` },
            { key: 'Profit Margin (%)', format: (v) => `${v?.toFixed(2)}%` },
            { key: '5Y CAGR (%)', format: (v) => `${v?.toFixed(2)}%` },
            { key: 'Revenue Growth (%)', format: (v) => `${v?.toFixed(2)}%` },
            { key: 'EPS Growth (%)', format: (v) => `${v?.toFixed(2)}%` },
            { key: 'Revenue Growth (3Y)', format: (v) => `${(v * 100)?.toFixed(2)}%` },
            { key: 'Earnings Growth (3Y)', format: (v) => `${(v * 100)?.toFixed(2)}%` }
        ],
        'Dividend & Financial Health': [
            { key: 'Dividend Yield (%)', format: (v) => `${v?.toFixed(2)}%` },
            { key: 'Dividend Payout Ratio (%)', format: (v) => `${v?.toFixed(2)}%` },
            { key: 'Debt/Equity', format: (v) => v?.toFixed(2) || 'N/A' },
            { key: 'Current Ratio', format: (v) => v?.toFixed(2) || 'N/A' },
            { key: 'Free Cash Flow (B)', format: (v) => `$${v?.toFixed(2)}B` },
            { key: 'Operating Cash Flow (B)', format: (v) => `$${v?.toFixed(2)}B` }
        ],
        'Market & Ownership': [
            { key: 'Beta', format: (v) => v?.toFixed(2) || 'N/A' },
            { key: '52 Week High', format: (v) => `$${v?.toFixed(2)}` },
            { key: '52 Week Low', format: (v) => `$${v?.toFixed(2)}` },
            { key: 'Analyst Target Price', format: (v) => `$${v?.toFixed(2)}` },
            { key: 'Analyst Recommendation', format: (v) => v || 'N/A' },
            { key: 'Short % of Float', format: (v) => `${(v * 100)?.toFixed(2)}%` },
            { key: 'Institution %', format: (v) => `${(v * 100)?.toFixed(2)}%` },
            { key: 'Insider %', format: (v) => `${(v * 100)?.toFixed(2)}%` }
        ]
    };

    return (
        <div className="stock-detail">
            <button onClick={() => navigate('/')} className="back-button">
                ← Back to Stocks
            </button>

            <h1>{symbol} Stock Details</h1>

            {Object.entries(metricGroups).map(([groupName, metrics]) => (
                <div key={groupName} className="metric-group">
                    <h2>{groupName}</h2>
                    <div className="metrics-grid">
                        {metrics.map(({ key, format }) => (
                            <div key={key} className="metric-card">
                                <h3>{key}</h3>
                                <p>{format(stockData[key])}</p>
                            </div>
                        ))}
                    </div>
                </div>
            ))}

            <div className="stock-graph-container">
                <h2>Price History</h2>
                <StockGraph symbol={symbol} />
            </div>
        </div>
    );
};

export default StockDetail; 