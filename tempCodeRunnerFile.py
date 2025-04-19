import yfinance as yf
import pandas as pd

# List of NSE stock tickers (add more as needed)
nse_tickers = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS']

# Filters
min_price = 500
max_price = 4000
min_pe_ratio = 10
max_pe_ratio = 40

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            'Ticker': ticker,
            'Name': info.get('shortName'),
            'Current Price': info.get('currentPrice'),
            'P/E Ratio': info.get('trailingPE'),
            'Market Cap': info.get('marketCap'),
            '52 Week High': info.get('fiftyTwoWeekHigh'),
            '52 Week Low': info.get('fiftyTwoWeekLow'),
            'Volume': info.get('volume'),
            'Sector': info.get('sector'),
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Fetch data
data = [fetch_stock_data(ticker) for ticker in nse_tickers]
df = pd.DataFrame([d for d in data if d is not None])

# Apply filters
filtered = df[
    (df['Current Price'] >= min_price) &
    (df['Current Price'] <= max_price) &
    (df['P/E Ratio'] >= min_pe_ratio) &
    (df['P/E Ratio'] <= max_pe_ratio)
]

# Display
print("\nFiltered Stocks:\n")
print(filtered.to_string(index=False))
