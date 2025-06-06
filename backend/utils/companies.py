# NSE Nifty 50 companies
NSE_COMPANIES = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 'SBIN', 'BHARTIARTL',
    'KOTAKBANK', 'BAJFINANCE', 'LICI', 'LT', 'HCLTECH', 'ASIANPAINT', 'AXISBANK', 'MARUTI',
    'SUNPHARMA', 'TITAN', 'WIPRO', 'ONGC', 'NESTLEIND', 'POWERGRID', 'ULTRACEMCO', 'BAJAJFINSV',
    'JSWSTEEL', 'ADANIPORTS', 'TATASTEEL', 'HDFCLIFE', 'DRREDDY', 'BRITANNIA', 'GRASIM', 'DIVISLAB',
    'BAJAJ-AUTO', 'SHREECEM', 'HINDALCO', 'UPL', 'TECHM', 'TATACONSUM', 'COALINDIA', 'CIPLA',
    'HEROMOTOCO', 'EICHERMOT', 'ITC', 'SBILIFE', 'BPCL', 'INDUSINDBK', 'NTPC', 'M&M', 'TATAMOTORS'
]

# BSE Sensex 30 companies
BSE_COMPANIES = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 'SBIN', 'BHARTIARTL',
    'KOTAKBANK', 'BAJFINANCE', 'LT', 'HCLTECH', 'ASIANPAINT', 'AXISBANK', 'MARUTI', 'SUNPHARMA',
    'TITAN', 'WIPRO', 'ONGC', 'NESTLEIND', 'POWERGRID', 'ULTRACEMCO', 'BAJAJFINSV', 'JSWSTEEL',
    'TATASTEEL', 'HDFCLIFE', 'DRREDDY', 'BRITANNIA', 'INDUSINDBK', 'M&M'
]

# NSE Nifty Next 50 companies
NSE_NEXT_50 = [
    'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ADANITRANS', 'ATGL', 'AMBUJACEM', 'APOLLOHOSP', 'ASIANPAINT',
    'AUROPHARMA', 'DMART', 'BAJAJHLDNG', 'BAJFINANCE', 'BAJAJFINSV', 'BPCL', 'BHARTIARTL', 'BRITANNIA',
    'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GAIL', 'GRASIM', 'HCLTECH', 'HDFCBANK',
    'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'INDUSINDBK',
    'INFY', 'ITC', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'NTPC', 'ONGC', 'POWERGRID',
    'RELIANCE', 'SBILIFE', 'SBIN', 'SUNPHARMA', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TCS', 'TECHM',
    'TITAN', 'ULTRACEMCO', 'UPL', 'WIPRO'
]

# BSE 100 companies (excluding Sensex 30)
BSE_100 = [
    'ABB', 'ACC', 'ADANIENT', 'ADANIPORTS', 'AMBUJACEM', 'ASHOKLEY', 'AUROPHARMA', 'AXISBANK', 'BAJAJ-AUTO',
    'BAJAJFINSV', 'BAJFINANCE', 'BANKBARODA', 'BERGEPAINT', 'BHARATFORG', 'BHARTIARTL', 'BOSCHLTD', 'BPCL',
    'BRITANNIA', 'CADILAHC', 'CANBK', 'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COLPAL', 'CONCOR', 'CUMMINSIND',
    'DABUR', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'ESCORTS', 'EXIDEIND', 'FEDERALBNK', 'GAIL', 'GLENMARK',
    'GODREJCP', 'GRASIM', 'HAVELLS', 'HCLTECH', 'HDFC', 'HDFCBANK', 'HEROMOTOCO', 'HINDALCO', 'HINDPETRO',
    'HINDUNILVR', 'IBULHSGFIN', 'ICICIBANK', 'ICICIPRULI', 'IDEA', 'IDFCFIRSTB', 'IGL', 'INDUSINDBK', 'INFY',
    'IOC', 'ITC', 'JSWSTEEL', 'JUBLFOOD', 'KOTAKBANK', 'LICHSGFIN', 'LT', 'LUPIN', 'M&M', 'MARICO', 'MARUTI',
    'MCDOWELL-N', 'MOTHERSUMI', 'MRF', 'MUTHOOTFIN', 'NATIONALUM', 'NESTLEIND', 'NMDC', 'NTPC', 'ONGC',
    'PAGEIND', 'PEL', 'PETRONET', 'PIDILITIND', 'POWERGRID', 'RELIANCE', 'SAIL', 'SBIN', 'SHREECEM', 'SIEMENS',
    'SRF', 'SUNPHARMA', 'TATACHEM', 'TATACONSUM', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TCS', 'TECHM',
    'TITAN', 'TORNTPHARM', 'TORNTPOWER', 'TVSMOTOR', 'ULTRACEMCO', 'UPL', 'VEDL', 'VOLTAS', 'WIPRO', 'ZEEL'
]

# Combine all companies
ALL_COMPANIES = list(set(NSE_COMPANIES + BSE_COMPANIES + NSE_NEXT_50 + BSE_100)) 