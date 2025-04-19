// src/pages/Screener.jsx
import React, { useState } from 'react';
import API from '../api';
import '../styles/Screener.css';

const Screener = () => {
  const [filters, setFilters] = useState({
    exchange: '',
    // Valuation Metrics
    pe: '',
    pb: '',
    ps: '',
    peg: '',
    enterpriseToEbitda: '',
    // Profitability Metrics
    roe: '',
    roce: '',
    roa: '',
    operatingMargin: '',
    profitMargin: '',
    // Growth Metrics
    revenueGrowth: '',
    earningsGrowth: '',
    cagr5Y: '',
    // Financial Health
    marketCap: '',
    debtToEquity: '',
    currentRatio: '',
    quickRatio: '',
    interestCoverage: '',
    // Dividend Metrics
    dividendYield: '',
    payoutRatio: '',
    dividendGrowth: '',
    // Per Share Metrics
    eps: '',
    bookValuePerShare: '',
    cashPerShare: '',
    // Price Information
    priceToCashFlow: '',
    priceToFreeCashFlow: '',
    // Volume and Liquidity
    avgVolume: '',
    beta: ''
  });

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('valuation'); // Default to valuation metrics

  const handleFilter = () => {
    setLoading(true);
    API.post('/screener/filter', filters)
      .then(res => {
        setResults(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value ? (name === 'exchange' ? value : Number(value)) : ''
    }));
  };

  const metricGroups = {
    valuation: {
      title: 'Valuation Metrics',
      metrics: [
        { name: 'pe', label: 'P/E Ratio', placeholder: 'Max P/E' },
        { name: 'pb', label: 'P/B Ratio', placeholder: 'Max P/B' },
        { name: 'ps', label: 'P/S Ratio', placeholder: 'Max P/S' },
        { name: 'peg', label: 'PEG Ratio', placeholder: 'Max PEG' },
        { name: 'enterpriseToEbitda', label: 'EV/EBITDA', placeholder: 'Max EV/EBITDA' }
      ]
    },
    profitability: {
      title: 'Profitability Metrics',
      metrics: [
        { name: 'roe', label: 'ROE (%)', placeholder: 'Min ROE' },
        { name: 'roce', label: 'ROCE (%)', placeholder: 'Min ROCE' },
        { name: 'roa', label: 'ROA (%)', placeholder: 'Min ROA' },
        { name: 'operatingMargin', label: 'Operating Margin (%)', placeholder: 'Min Margin' },
        { name: 'profitMargin', label: 'Profit Margin (%)', placeholder: 'Min Margin' }
      ]
    },
    growth: {
      title: 'Growth Metrics',
      metrics: [
        { name: 'revenueGrowth', label: 'Revenue Growth (%)', placeholder: 'Min Growth' },
        { name: 'earningsGrowth', label: 'Earnings Growth (%)', placeholder: 'Min Growth' },
        { name: 'cagr5Y', label: '5-Year CAGR (%)', placeholder: 'Min CAGR' }
      ]
    },
    financialHealth: {
      title: 'Financial Health',
      metrics: [
        { name: 'marketCap', label: 'Market Cap (Cr)', placeholder: 'Min Market Cap' },
        { name: 'debtToEquity', label: 'Debt to Equity', placeholder: 'Max D/E' },
        { name: 'currentRatio', label: 'Current Ratio', placeholder: 'Min Ratio' },
        { name: 'quickRatio', label: 'Quick Ratio', placeholder: 'Min Ratio' },
        { name: 'interestCoverage', label: 'Interest Coverage', placeholder: 'Min Coverage' }
      ]
    },
    dividend: {
      title: 'Dividend Metrics',
      metrics: [
        { name: 'dividendYield', label: 'Dividend Yield (%)', placeholder: 'Min Yield' },
        { name: 'payoutRatio', label: 'Payout Ratio (%)', placeholder: 'Max Ratio' },
        { name: 'dividendGrowth', label: 'Dividend Growth (%)', placeholder: 'Min Growth' }
      ]
    }
  };

  return (
    <div className="screener-container">
      <h1 className="screener-title">Stock Screener</h1>
      
      <div className="filters-section">
        <div className="exchange-filter">
          <div className="filter-group">
            <label>Exchange</label>
            <select
              name="exchange"
              value={filters.exchange}
              onChange={handleInputChange}
            >
              <option value="">All Exchanges</option>
              <option value="NSE">NSE</option>
              <option value="BSE">BSE</option>
            </select>
          </div>
        </div>

        <div className="metric-tabs">
          {Object.keys(metricGroups).map(group => (
            <button
              key={group}
              className={`tab-button ${activeTab === group ? 'active' : ''}`}
              onClick={() => setActiveTab(group)}
            >
              {metricGroups[group].title}
            </button>
          ))}
        </div>

        <div className="filters-grid">
          {metricGroups[activeTab].metrics.map(metric => (
            <div className="filter-group" key={metric.name}>
              <label>{metric.label}</label>
              <input
                type="number"
                name={metric.name}
                value={filters[metric.name]}
                onChange={handleInputChange}
                placeholder={metric.placeholder}
              />
            </div>
          ))}
        </div>
      </div>

      <button 
        className="filter-button"
        onClick={handleFilter}
        disabled={loading}
      >
        {loading ? 'Filtering...' : 'Apply Filters'}
      </button>

      {results.length > 0 && (
        <div className="results-container">
          <h2>Results ({results.length})</h2>
          <div className="results-table">
            <table>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Name</th>
                  <th>Exchange</th>
                  <th>Sector</th>
                  <th>Price</th>
                  <th>P/E</th>
                  <th>P/B</th>
                  <th>P/S</th>
                  <th>ROE</th>
                  <th>ROCE</th>
                  <th>Market Cap</th>
                  <th>D/E</th>
                  <th>Current Ratio</th>
                  <th>Dividend Yield</th>
                </tr>
              </thead>
              <tbody>
                {results.map(stock => (
                  <tr key={stock.symbol}>
                    <td>{stock.symbol}</td>
                    <td>{stock.name}</td>
                    <td>{stock.exchange}</td>
                    <td>{stock.sector}</td>
                    <td>₹{stock.price}</td>
                    <td>{stock.pe}</td>
                    <td>{stock.pb}</td>
                    <td>{stock.ps}</td>
                    <td>{stock.roe}%</td>
                    <td>{stock.roce}%</td>
                    <td>₹{stock.marketCap} Cr</td>
                    <td>{stock.debtToEquity}</td>
                    <td>{stock.currentRatio}</td>
                    <td>{stock.dividendYield}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Screener;
