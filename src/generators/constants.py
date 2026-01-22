COUNTRY_WEIGHTS = {
    'US': 0.30,
    'BR': 0.17,
    'IN': 0.13,
    'GB': 0.12,
    'DE': 0.10,
    'FR': 0.08,
    'CA': 0.06,
    'AU': 0.04
}


RISK_PROFILES = [
    1, # conservative 
    2, # moderate
    3 # aggressive
]

BROKERAGES = [
    'ddb1a914-69d7-494e-9f73-6677ba2c222e',
    'af5aae3a-9ed0-4b64-90c7-139bea178467',
    'b5eb4b52-8dda-41e9-afb2-ebbcbe59f886'
]

ACCOUNT_TYPES = {
    'cash': 1, 
    'margin': 2,
    'retirement': 3
}

CURRENCIES = {
    'USD':1,
    'EUR':2,
    'BRL':3
}

TRADE_TYPES = [
    1, #buy
    2 #sell
]

ASSETS = [
    # Stocks
    ('AAPL', 'Apple Inc.', 'stock', 'USD'),
    ('MSFT', 'Microsoft Corporation', 'stock', 'USD'),
    ('NVDA', 'NVIDIA Corporation', 'stock', 'USD'),
    ('TM', 'Toyota Motor Corporation', 'stock', 'USD'), 
    ('SAP', 'SAP SE', 'stock', 'EUR'),

    # ETFs
    ('SPY', 'SPDR S&P 500 ETF', 'etf', 'USD'),
    ('QQQ', 'Invesco QQQ ETF', 'etf', 'USD'),
    ('VT', 'Vanguard Total World ETF', 'etf', 'USD'),

    # Bonds
    ('US10Y', 'US Treasury 10Y', 'bond', 'USD'),
    ('BR10Y', 'Brazil Gov Bond 10Y', 'bond', 'BRL'),

    # Crypto
    ('BTC', 'Bitcoin', 'crypto', 'USD'),
    ('ETH', 'Ethereum', 'crypto', 'USD'),
]

ASSET_TYPES = {
    'stock': 1,
    'etf': 2,
    'bond': 3,
    'crypto': 4,
}