from flask import Flask
from flask_cors import CORS
from routes.market import market_bp
from routes.screener import screener_bp
from routes.ai import ai_bp
from routes.patterns import patterns_bp
from routes.stock import stock_bp
from dotenv import load_dotenv
from utils.db import init_db
import logging

load_dotenv()

app = Flask(__name__)
# Configure CORS with specific settings
CORS(app, resources={
    r"/*": {
        "origins": ["https://groqsense-rphz.onrender.com", "http://localhost:3000", "http://localhost:5173", "https://groqsense.onrender.com"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
    }
})

# Register Blueprints
app.register_blueprint(market_bp, url_prefix="/market")
app.register_blueprint(screener_bp, url_prefix="/screener")
app.register_blueprint(ai_bp, url_prefix="/ai")
app.register_blueprint(patterns_bp, url_prefix="/patterns")
app.register_blueprint(stock_bp, url_prefix="/api/stock")

@app.route("/")
def home():
    return {"message": "GroqSense Backend is Running ✅"}

# Initialize database tables
try:
    logging.info("Initializing database tables...")
    init_db()
    logging.info("Database tables initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing database tables: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
