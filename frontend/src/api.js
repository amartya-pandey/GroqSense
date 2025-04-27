import axios from 'axios';

const API = axios.create({
  baseURL: 'https://groqsense.onrender.com', // Updated to use correct deployed backend URL
});

export default API;
