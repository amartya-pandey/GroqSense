import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Screener from './pages/Screener';
import Assistant from './pages/Assistant';
import Patterns from './pages/Patterns';
import Navbar from './components/Navbar';
import StockDetail from './pages/StockDetail';

const App = () => (
  <Router>
    <Navbar />
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/screener" element={<Screener />} />
      <Route path="/assistant" element={<Assistant />} />
      <Route path="/patterns" element={<Patterns />} />
      <Route path="/stock/:symbol" element={<StockDetail />} />
    </Routes>
  </Router>
);

export default App;
