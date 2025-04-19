import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of Indian stocks (tickers for yfinance + Screener code)
stock_map = {
    'RELIANCE': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'HDFCBANK': 'HDFCBANK.NS',
    'INFY': 'INFY.NS',
    'ICICIBANK': 'ICICIBANK.NS'
}

def get_yfinance_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'Market Cap': info.get('marketCap'),
            'Dividend Yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else None,
            'Current Price': info.get('currentPrice')
        }
    except Exception as e:
        print(f"Error fetching yfinance data for {ticker}: {e}")
        return {}

ratios = {}
def get_screener_data(stock_code):
    try:
        url = f"https://www.screener.in/company/{stock_code}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        data = {
            "P/E Ratio": None,
            "P/B Ratio": None,
            "ROE": None,
            "ROCE": None,
            "5Y CAGR": None,
            "Debt to Equity": None
        }

        # Find quick ratio pairs
        for li in soup.select("ul.ranges li"):
            key = li.select_one(".name")
            val = li.select_one(".value")
            if key and val:
                k = key.text.strip()
                v = val.text.strip()

                if k == "P/E":
                    data["P/E Ratio"] = v
                elif k == "P/B":
                    data["P/B Ratio"] = v
                elif k == "ROE":
                    data["ROE"] = v
                elif k == "ROCE":
                    data["ROCE"] = v
                elif k == "Debt to equity":
                    data["Debt to Equity"] = v

        # Get 5Y CAGR (Compounded Sales Growth)
        growth_table = soup.find("section", id="profit-loss")
        if growth_table:
            growth_row = soup.find(string="Compounded Sales Growth")
            if growth_row:
                row = growth_row.find_parent("tr")
                if row:
                    cells = row.find_all("td")
                    if len(cells) > 5:
                        data["5Y CAGR"] = cells[5].text.strip()

        return data

    except Exception as e:
        print(f"Error parsing Screener data for {stock_code}: {e}")
        return {}

# # Gather all data
# all_data = []

# for screener_code, yf_ticker in stock_map.items():
#     print(f"Fetching data for {screener_code}...")
#     time.sleep(1.5)  # be kind to Screener.in

#     screener_data = get_screener_data(screener_code)
#     yf_data = get_yfinance_data(yf_ticker)

#     combined = {'Stock': screener_code}
#     combined.update(screener_data)
#     combined.update(yf_data)

#     all_data.append(combined)

# # Create dataframe
# df = pd.DataFrame(all_data)
# print(df)

# # Optional: filter e.g., PE < 30 and ROE > 15
# filtered_df = df[
#     (df['P/E Ratio'].astype(float) < 30) &
#     (df['ROE'].str.replace('%','').astype(float) > 15)
# ]

# print(ratios)
# # print("\nFiltered Screener Results:")
# # print(filtered_df)

print(get_screener_data("RELIANCE"))
