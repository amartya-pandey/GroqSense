import React, { useState } from 'react';
import API from '../api';
import MarkdownIt from 'markdown-it';
import '../styles/Assistant.css'; // Import the new CSS file

const Assistant = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const md = new MarkdownIt();

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
    <div className="assistant-container">
      <h2 className="assistant-title">AI Assistant</h2>
      <textarea
        className="assistant-textarea"
        rows={4}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask your question..."
      />
      <button className="assistant-button" onClick={handleAsk} disabled={loading}>
        {loading ? 'Thinking...' : 'Ask'}
      </button>
      {error && <p className="assistant-error">{error}</p>}
      {response && (
        <div
          className="assistant-response"
          dangerouslySetInnerHTML={{ __html: md.render(response) }}
        />
      )}
    </div>
  );
};

export default Assistant;