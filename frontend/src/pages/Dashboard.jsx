// src/pages/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import API from '../api';

const Dashboard = () => {
  const [indices, setIndices] = useState({});

  useEffect(() => {
    API.get('/market/indices')
      .then((res) => setIndices(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h1>Indian Market Indices</h1>
      <ul>
        {Object.entries(indices).map(([name, data]) => (
          <li key={name}>
            {name}: ₹{data.price} ({data.symbol})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
