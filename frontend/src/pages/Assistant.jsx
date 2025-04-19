import React, { useState } from 'react';
import API from '../api';

const Assistant = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAsk = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setResponse('');

    try {
      const res = await API.post('/ai/query', { query });
      setResponse(res.data.answer || 'No answer returned');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>AI Assistant</h2>
      <textarea
        rows={4}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask your stock question..."
        style={{ width: '100%', padding: '10px' }}
      />
      <br />
      <button onClick={handleAsk} disabled={loading}>
        {loading ? 'Thinking...' : 'Ask'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {response && <div style={{ marginTop: '20px', whiteSpace: 'pre-line' }}>{response}</div>}
    </div>
  );
};

export default Assistant;
