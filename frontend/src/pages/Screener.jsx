// src/pages/Screener.jsx
import React, { useState, useEffect } from 'react';
import API from '../api';
import '../styles/Screener.css';

// Define which metrics should use <= for filtering
const LOWER_BOUND_METRICS = new Set([
  'pe', 'pb', 'debtToEquity', 'beta', 'priceToCashFlow', 'priceToFreeCashFlow'
]);

const Screener = () => {
  const [filters, setFilters] = useState({
    pe: '', pb: '', bookValue: '', eps: '', dividendYield: '',
    roe: '', cagr5Y: '', debtToEquity: '', marketCap: '',
    beta: '', avgVolume: '', cashPerShare: '',
    priceToCashFlow: '', priceToFreeCashFlow: ''
  });

  const [exchange, setExchange] = useState('both');
  const [index, setIndex] = useState('all');
  const [allStocks, setAllStocks] = useState([]);
  const [filteredStocks, setFilteredStocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('valuation');

  const indexOptions = [
    { value: 'all', label: 'All Companies' },
    { value: 'nifty50', label: 'NSE Nifty 50' },
    { value: 'niftynext50', label: 'NSE Next 50' },
    { value: 'sensex30', label: 'BSE Sensex 30' },
    { value: 'bse100', label: 'BSE 100' }
  ];

  const metricGroups = {
    valuation: {
      title: 'Valuation Metrics',
      metrics: [
        { key: 'pe', label: 'P/E Ratio', placeholder: 'Enter max P/E' },
        { key: 'pb', label: 'P/B Ratio', placeholder: 'Enter max P/B' },
        { key: 'bookValue', label: 'Book Value', placeholder: 'Enter min Book Value' },
        { key: 'eps', label: 'Earnings Per Share', placeholder: 'Enter min EPS' },
        { key: 'priceToCashFlow', label: 'Price/Cash Flow', placeholder: 'Enter max P/CF' },
        { key: 'priceToFreeCashFlow', label: 'Price/FCF', placeholder: 'Enter max P/FCF' }
      ]
    },
    profitability: {
      title: 'Profitability Metrics',
      metrics: [
        { key: 'roe', label: 'ROE (%)', placeholder: 'Enter min ROE' },
        { key: 'cagr5Y', label: '5Y CAGR (%)', placeholder: 'Enter min CAGR' }
      ]
    },
    financialHealth: {
      title: 'Financial Health',
      metrics: [
        { key: 'debtToEquity', label: 'Debt to Equity', placeholder: 'Enter max Debt/Equity' },
        { key: 'marketCap', label: 'Market Cap (Cr)', placeholder: 'Enter min Market Cap' }
      ]
    },
    technical: {
      title: 'Technical Metrics',
      metrics: [
        { key: 'beta', label: 'Beta', placeholder: 'Enter max Beta' },
        { key: 'avgVolume', label: 'Avg Volume', placeholder: 'Enter min Volume' }
      ]
    }
  };

  const columns = [
    { field: 'symbol', headerName: 'Symbol' },
    { field: 'name', headerName: 'Company' },
    { field: 'exchange', headerName: 'Exchange' },
    { field: 'price', headerName: 'Price' },
    { field: 'pe', headerName: 'P/E' },
    { field: 'pb', headerName: 'P/B' },
    { field: 'bookValue', headerName: 'Book Value' },
    { field: 'eps', headerName: 'Diluted EPS' },
    // { field: 'cagr5Y', headerName: '5Y CAGR (%)' },
    { field: 'marketCap', headerName: 'Market Cap (Cr)' },
    // { field: 'dividendYield', headerName: 'Div Yield (%)' },
    { field: 'beta', headerName: 'Beta' },
    { field: 'avgVolume', headerName: 'Avg Volume' },
    { field: 'debtToEquity', headerName: 'Debt/Equity' },
    { field: 'roe', headerName: 'ROE (%)' },
  ];

  const fetchStocks = async () => {
    setLoading(true);
    try {
      console.log('Fetching stocks with:', { exchange, index });
      const response = await API.post('/screener/filter', {
        filters: {},
        exchange: exchange,
        index: index
      });
      console.log('Received stocks:', response.data);
      setAllStocks(response.data);
      setFilteredStocks(response.data);
    } catch (error) {
      console.error('Error fetching stocks:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = async () => {
    if (allStocks.length === 0) {
      console.log('No stocks available to filter');
      return;
    }

    console.log('Applying filters:', filters);
    const activeFilters = Object.entries(filters).filter(([_, value]) => value !== '');
    console.log('Active filters:', activeFilters);

    if (activeFilters.length === 0) {
      console.log('No active filters, showing all stocks');
      setFilteredStocks(allStocks);
      return;
    }

    const filtered = allStocks.filter(stock => {
      return activeFilters.every(([key, value]) => {
        const stockValue = stock[key];
        console.log(`Checking ${key}: stock value = ${stockValue}, filter value = ${value}`);

        if (stockValue === undefined || stockValue === null) {
          console.log(`Skipping ${key} - no value available`);
          return false;
        }

        const filterNum = Number(value);
        const stockNum = Number(stockValue);
        const isLowerBound = LOWER_BOUND_METRICS.has(key);
        const passesFilter = isLowerBound ? stockNum <= filterNum : stockNum >= filterNum;

        console.log(`${key} comparison: ${stockNum} ${isLowerBound ? '<=' : '>='} ${filterNum} = ${passesFilter}`);
        return passesFilter;
      });
    });

    console.log('Filtered results:', filtered);
    setFilteredStocks(filtered);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (value === '' || !isNaN(value)) {
      setFilters(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  return (
    <div className="screener-container">
      <h1>Stock Screener</h1>
      
      <div className="filters-section">
        <div className="filter-row">
          <div className="exchange-filter">
            <label>Exchange:</label>
            <select 
              value={exchange} 
              onChange={(e) => setExchange(e.target.value)}
              className="exchange-select"
            >
              <option value="both">Both NSE & BSE</option>
              <option value="nse">NSE Only</option>
              <option value="bse">BSE Only</option>
            </select>
          </div>

          <div className="index-filter">
            <label>Index:</label>
            <select 
              value={index} 
              onChange={(e) => setIndex(e.target.value)}
              className="index-select"
            >
              {indexOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
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
            <div className="filter-group" key={metric.key}>
              <label>{metric.label}</label>
      <input
        type="number"
                name={metric.key}
                value={filters[metric.key]}
                onChange={handleInputChange}
                placeholder={metric.placeholder}
                min="0"
                step="0.01"
              />
            </div>
          ))}
        </div>

        <div className="button-group">
          <button 
            className="filter-button fetch-all"
            onClick={fetchStocks}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Fetch Stocks'}
          </button>
          <button 
            className="filter-button apply-filters"
            onClick={applyFilters}
            disabled={loading || allStocks.length === 0}
          >
            Apply Filters
          </button>
        </div>
      </div>

      {filteredStocks.length > 0 && (
        <div className="results-section">
          <h2>Results ({filteredStocks.length})</h2>
          <div className="results-table">
            <table>
              <thead>
                <tr>
                  {columns.map(column => (
                    <th key={column.field}>{column.headerName}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filteredStocks.map((row, index) => (
                  <tr key={index}>
                    {columns.map(column => (
                      <td key={column.field}>{row[column.field]}</td>
                    ))}
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
