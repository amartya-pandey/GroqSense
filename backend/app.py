from flask import Flask
from flask_cors import CORS
from routes.market import market_bp
from routes.screener import screener_bp
from routes.ai import ai_bp
from routes.patterns import patterns_bp
from routes.stock import stock_bp
from dotenv import load_dotenv
from utils.db import init_db

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(market_bp, url_prefix="/market")
app.register_blueprint(screener_bp, url_prefix="/screener")
app.register_blueprint(ai_bp, url_prefix="/ai")
app.register_blueprint(patterns_bp, url_prefix="/patterns")
app.register_blueprint(stock_bp, url_prefix="/api/stock")

@app.route("/")
def home():
    return {"message": "GroqSense Backend is Running ✅"}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
