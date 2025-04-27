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
            { key: 'price', label: 'Current Price', format: (v) => v !== undefined && v !== null ? `$${v.toFixed(2)}` : 'N/A' },
            { key: 'marketCap', label: 'Market Cap', format: (v) => v !== undefined && v !== null ? `$${v.toLocaleString()}` : 'N/A' },
            { key: 'pe', label: 'P/E Ratio', format: (v) => v !== undefined && v !== null ? v.toFixed(2) : 'N/A' },
            { key: 'pb', label: 'P/B Ratio', format: (v) => v !== undefined && v !== null ? v.toFixed(2) : 'N/A' },
            { key: 'bookValue', label: 'Book Value', format: (v) => v !== undefined && v !== null ? v.toFixed(2) : 'N/A' },
            { key: 'eps', label: 'EPS', format: (v) => v !== undefined && v !== null ? v.toFixed(2) : 'N/A' },
            { key: 'dividendYield', label: 'Dividend Yield', format: (v) => v !== undefined && v !== null ? `${(v * 100).toFixed(2)}%` : 'N/A' },
        ],
        'Profitability': [
            { key: 'roe', label: 'ROE', format: (v) => v !== undefined && v !== null ? `${(v * 100).toFixed(2)}%` : 'N/A' },
        ],
        'Technical': [
            { key: 'beta', label: 'Beta', format: (v) => v !== undefined && v !== null ? v.toFixed(2) : 'N/A' },
            { key: 'avgVolume', label: 'Avg Volume', format: (v) => v !== undefined && v !== null ? v.toLocaleString() : 'N/A' },
        ],
        'Other': [
            { key: 'symbol', label: 'Symbol', format: (v) => v || 'N/A' },
            { key: 'name', label: 'Company Name', format: (v) => v || 'N/A' },
            { key: 'exchange', label: 'Exchange', format: (v) => v || 'N/A' },
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
                        {metrics.map(({ key, label, format }) => (
                            <div key={key} className="metric-card">
                                <h3>{label}</h3>
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