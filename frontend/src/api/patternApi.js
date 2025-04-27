const API_BASE_URL = 'http://localhost:5000/patterns';

export const patternApi = {
    detectPatterns: async (symbol, period = '1y') => {
        try {
            const response = await fetch(`${API_BASE_URL}/detect-patterns`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symbol, period }),
            });
            return await response.json();
        } catch (error) {
            console.error('Error detecting patterns:', error);
            throw error;
        }
    },

    analyzeChart: async (symbol, query, period = '1y') => {
        try {
            const response = await fetch(`${API_BASE_URL}/analyze-chart`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symbol, query, period }),
            });
            return await response.json();
        } catch (error) {
            console.error('Error analyzing chart:', error);
            throw error;
        }
    },

    analyzeTrends: async (symbol, period = '1y', trendData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/analyze-trends`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symbol, period, trend_data: trendData }),
            });
            return await response.json();
        } catch (error) {
            console.error('Error analyzing trends:', error);
            throw error;
        }
    }
}; 