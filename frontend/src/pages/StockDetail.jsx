import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import StockGraph from '../components/StockGraph';
import API_BASE_URL from '../api/config';

const StockDetail = () => {
    const { symbol } = useParams();
    const navigate = useNavigate();
    const [stockData, setStockData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStockData = async () => {
            try {
                setLoading(true);
                const response = await axios.get(`${API_BASE_URL}/api/stock/${symbol}`);
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
        return <div className="loading" style={{ textAlign: 'center', marginTop: '100px', fontSize: '24px', fontWeight: '600' }}>Loading stock data...</div>;
    }

    if (!stockData) {
        return <div className="error" style={{ textAlign: 'center', marginTop: '100px', fontSize: '24px', color: 'red', fontWeight: '600' }}>Error loading stock data</div>;
    }

    const metricGroups = {
        'Valuation': [
            { key: 'price', label: 'Current Price', format: (v) => v !== undefined && v !== null ? `₹${v.toFixed(2)}` : 'N/A' },
            { key: 'marketCap', label: 'Market Cap', format: (v) => v !== undefined && v !== null ? `₹${v.toLocaleString()}` : 'N/A' },
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
        <div className="stock-detail" style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
            <button 
                onClick={() => navigate('/')} 
                className="back-button" 
                style={{
                    backgroundColor: '#007bff',
                    color: '#fff',
                    border: 'none',
                    padding: '10px 20px',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    marginBottom: '20px',
                    fontWeight: '600',
                    transition: 'background 0.3s',
                }}
                onMouseOver={e => e.target.style.backgroundColor = '#0056b3'}
                onMouseOut={e => e.target.style.backgroundColor = '#007bff'}
            >
                ← Back to Stocks
            </button>

            <h1 style={{ fontSize: '32px', fontWeight: '700', marginBottom: '30px', color: '#333' }}>{symbol} Stock Details</h1>

            <div className="metrics-section">
                <h2 className="metrics-title" style={{ fontSize: '26px', fontWeight: '600', marginBottom: '20px', color: '#555' }}>Key Metrics</h2>
                {Object.entries(metricGroups).map(([groupName, metrics]) => (
                    <div key={groupName} className="metric-group" style={{ marginBottom: '40px' }}>
                        <h3 style={{ fontSize: '22px', fontWeight: '600', color: '#666', marginBottom: '10px' }}>{groupName}</h3>
                        <div className="metrics-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
                            {metrics.map(({ key, label, format }) => (
                                <div 
                                    key={key} 
                                    className="metric-card"
                                    style={{
                                        backgroundColor: '#f9f9f9',
                                        padding: '15px',
                                        borderRadius: '10px',
                                        boxShadow: '0 4px 6px rgba(0,0,0,0.05)',
                                        transition: 'transform 0.2s',
                                    }}
                                    onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.03)'}
                                    onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
                                >
                                    <h4 style={{ fontSize: '18px', fontWeight: '500', color: '#333' }}>{label}</h4>
                                    <p style={{ fontSize: '20px', fontWeight: '700', marginTop: '10px', color: '#111' }}>{format(stockData[key])}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            <div className="stock-graph-container" style={{ marginTop: '60px' }}>
                <h2 style={{ fontSize: '26px', fontWeight: '600', color: '#555', marginBottom: '20px' }}>Price History</h2>
                <div style={{
                    backgroundColor: '#fff',
                    padding: '20px',
                    borderRadius: '10px',
                    boxShadow: '0 4px 8px rgba(0,0,0,0.08)'
                }}>
                    <StockGraph symbol={symbol} />
                </div>
            </div>
        </div>
    );
};

export default StockDetail;
