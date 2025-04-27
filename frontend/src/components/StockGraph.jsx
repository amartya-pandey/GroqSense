import React, { useState, useEffect } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';
import axios from 'axios';
import API_BASE_URL from '../api/config';
import './StockGraph.css';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend
);

// Clean array: only allow numbers, replace others with null (Chart.js skips null)
const cleanArray = arr => arr ? arr.map(v => (typeof v === 'number' && !isNaN(v) ? v : null)) : [];
// Limit number of points for performance
const MAX_POINTS = 200;
const sliceData = arr => arr.length > MAX_POINTS ? arr.slice(-MAX_POINTS) : arr;

const StockGraph = ({ symbol }) => {
    console.log('StockGraph received symbol:', symbol);
    const [timeRange, setTimeRange] = useState('1m');
    const [priceChartData, setPriceChartData] = useState(null);
    const [volumeChartData, setVolumeChartData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const timeRanges = {
        '5d': '5 Days',
        '1w': '1 Week',
        '1m': '1 Month',
        '6m': '6 Months',
        '1y': '1 Year',
        '5y': '5 Years'
    };

    useEffect(() => {
        const fetchStockData = async () => {
            try {
                setLoading(true);
                setError('');
                const response = await axios.get(`${API_BASE_URL}/api/stock/historical/${symbol}?range=${timeRange}`);
                console.log('API response data:', response.data);
                const data = response.data;

                if (!data.prices || data.prices.length === 0) {
                    setError('No price data available for this stock and range.');
                    setPriceChartData(null);
                    setVolumeChartData(null);
                    return;
                }

                // Clean and slice data for plotting
                const cleanedPrices = sliceData(cleanArray(data.prices));
                const cleanedVolumes = sliceData(cleanArray(data.volumes));
                const cleanedDates = sliceData(data.dates);

                setPriceChartData({
                    labels: cleanedDates,
                    datasets: [
                        {
                            label: `${symbol} Price`,
                            data: cleanedPrices,
                            borderColor: 'rgb(75, 192, 192)',
                            backgroundColor: 'rgba(75, 192, 192, 0.5)',
                            tension: 0.1,
                        }
                    ]
                });

                setVolumeChartData({
                    labels: cleanedDates,
                    datasets: [
                        {
                            label: 'Volume',
                            data: cleanedVolumes,
                            backgroundColor: 'rgba(201, 203, 207, 0.5)',
                            borderColor: 'rgba(201, 203, 207, 1)',
                            type: 'bar',
                        }
                    ]
                });
            } catch (error) {
                setError('Error fetching stock data.');
                setPriceChartData(null);
                setVolumeChartData(null);
                console.error('Error fetching stock data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStockData();
    }, [symbol, timeRange]);

    const priceOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: `${symbol} Price History`
            }
        },
        scales: {
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                    display: true,
                    text: 'Price'
                }
            }
        }
    };

    const volumeOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: `${symbol} Volume History`
            }
        },
        scales: {
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                    display: true,
                    text: 'Volume'
                }
            }
        }
    };

    return (
        <div className="stock-graph">
            <div className="graph-controls">
                <div className="time-range-buttons">
                    {Object.entries(timeRanges).map(([key, label]) => (
                        <button
                            key={key}
                            onClick={() => setTimeRange(key)}
                            className={timeRange === key ? 'active' : ''}
                        >
                            {label}
                        </button>
                    ))}
                </div>
            </div>

            {loading ? (
                <div className="loading">Loading chart data...</div>
            ) : error ? (
                <div className="error">{error}</div>
            ) : (
                <>
                    {priceChartData && <Line data={priceChartData} options={priceOptions} />}
                    {volumeChartData && <Bar data={volumeChartData} options={volumeOptions} />}
                </>
            )}
        </div>
    );
};

export default StockGraph; 