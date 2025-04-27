# GroqSense

GroqSense is a full-stack stock analysis and pattern recognition platform powered by Groq LLMs. It provides stock screening, technical pattern detection, and AI-driven trend analysis for Indian stocks.

## Features
- **Stock Screener:** Filter stocks by valuation, profitability, financial health, and technical metrics.
- **Pattern Recognition:** Detects technical chart patterns and provides AI-generated trend summaries.
- **AI Assistant:** Ask financial questions and get answers powered by Groq LLMs.
- **Modern UI:** Built with React and Vite for a fast, responsive experience.

---

## Project Structure
```
GroqSense/
├── backend/         # Flask backend (API, pattern recognition, stock data)
├── frontend/        # React frontend (Vite)
└── README.md        # This file
```

---

## Getting Started (Local Development)

### Prerequisites
- Node.js (v18+ recommended)
- Python 3.9+
- [Groq API Key](https://console.groq.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/amartya-pandey/GroqSense.git
cd GroqSense
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Create a .env file and add your Groq API key:
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
# Run the backend
python app.py
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
- The frontend will run on `http://localhost:5173` (or similar)
- The backend will run on `http://localhost:5000`

---

## Deployment on Render

### Backend
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Environment Variables:**
  - `GROQ_API_KEY` (required)
- **Python Version:** 3.9

### Frontend
- **Root Directory:** `frontend`
- **Build Command:** `npm install && npm run build`
- **Publish Directory:** `dist`
- **Environment Variable (optional):**
  - `REACT_APP_API_URL=https://groqsense.onrender.com`

---

## Usage
- Use the Screener to filter and explore stocks.
- Click on a stock to view details (always redirects to `SYMBOL.NS` if no suffix).
- Use Pattern Recognition to analyze trends and detect patterns.
- Use the AI Assistant for financial queries.

---

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License
[MIT](LICENSE) 