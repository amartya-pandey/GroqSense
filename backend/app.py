from flask import Flask
from flask_cors import CORS
from routes.market import market_bp
from routes.screener import screener_bp
from routes.ai import ai_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(market_bp, url_prefix="/market")
app.register_blueprint(screener_bp, url_prefix="/screener")
app.register_blueprint(ai_bp, url_prefix="/ai")

@app.route("/")
def home():
    return {"message": "GroqSense Backend is Running ✅"}

if __name__ == "__main__":
    app.run(debug=True)
