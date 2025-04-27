import axios from 'axios';
import API_BASE_URL from './config';

export const detectPatterns = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/patterns/detect`, data);
    return response.data;
};

export const analyzeChart = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/patterns/analyze-chart`, data);
    return response.data;
};

export const analyzeTrends = async (symbol, period) => {
    const response = await axios.post(`${API_BASE_URL}/patterns/analyze-trends`, {
        symbol,
        period
    });
    return response.data;
}; 