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

const StockGraph = ({ symbol }) => {
    const [timeRange, setTimeRange] = useState('1m');
    const [chartData, setChartData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [showVolume, setShowVolume] = useState(true);
    const [showMA, setShowMA] = useState(true);

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
                const response = await axios.get(`/api/stock/historical/${symbol}?range=${timeRange}`);
                const data = response.data;

                const datasets = [
                    {
                        label: `${symbol} Price`,
                        data: data.prices,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.5)',
                        tension: 0.1,
                        yAxisID: 'y'
                    }
                ];

                // Add moving averages if enabled
                if (showMA) {
                    if (data.ma20) {
                        datasets.push({
                            label: '20-day MA',
                            data: data.ma20,
                            borderColor: 'rgb(255, 99, 132)',
                            borderDash: [5, 5],
                            tension: 0.1,
                            yAxisID: 'y'
                        });
                    }
                    if (data.ma50) {
                        datasets.push({
                            label: '50-day MA',
                            data: data.ma50,
                            borderColor: 'rgb(54, 162, 235)',
                            borderDash: [5, 5],
                            tension: 0.1,
                            yAxisID: 'y'
                        });
                    }
                }

                const chartData = {
                    labels: data.dates,
                    datasets: datasets
                };

                // Add volume data if enabled
                if (showVolume && data.volumes) {
                    chartData.datasets.push({
                        label: 'Volume',
                        data: data.volumes,
                        backgroundColor: 'rgba(201, 203, 207, 0.5)',
                        yAxisID: 'y1',
                        type: 'bar'
                    });
                }

                setChartData(chartData);
            } catch (error) {
                console.error('Error fetching stock data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStockData();
    }, [symbol, timeRange, showVolume, showMA]);

    const options = {
        responsive: true,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: `${symbol} Stock Price History`
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
            },
            y1: {
                type: 'linear',
                display: showVolume,
                position: 'right',
                title: {
                    display: true,
                    text: 'Volume'
                },
                grid: {
                    drawOnChartArea: false
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
                <div className="toggle-buttons">
                    <button
                        onClick={() => setShowVolume(!showVolume)}
                        className={showVolume ? 'active' : ''}
                    >
                        Volume
                    </button>
                    <button
                        onClick={() => setShowMA(!showMA)}
                        className={showMA ? 'active' : ''}
                    >
                        Moving Averages
                    </button>
                </div>
            </div>

            {loading ? (
                <div className="loading">Loading chart data...</div>
            ) : chartData ? (
                <Line data={chartData} options={options} />
            ) : (
                <div className="error">Error loading chart data</div>
            )}
        </div>
    );
};

export default StockGraph; 