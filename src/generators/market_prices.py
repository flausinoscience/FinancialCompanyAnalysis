import random
from datetime import datetime, timedelta
from .constants import TICKERS_WITH_NAMES

def gen_market_prices(assets, n):
    """Yields rows for 'Market_Price' without 'id' column (Postgres serial).
    columns: (asset_id, price_at, price, created_at, updated_at)
    """
    NOW = datetime.now()

    total_assets = len(TICKERS_WITH_NAMES)
    rows_per_asset = max(10, n // total_assets)
    
    # ~5 years of backfilled price history.
    start_date = (NOW - timedelta(days=365*5))
    
    for a in assets:
        asset_id = a[0]
        ticker = a[1]
        price = 20.0 + (abs(hash(ticker)) % 1000) * 0.1
        curr_date = start_date
        for _ in range(rows_per_asset):
            curr_date += timedelta(days=1)
            # no weekends allowed
            if curr_date.weekday() > 4:
                continue
            # random-walk with occasional shock
            drift = random.gauss(0, 0.001)
            shock = 0.0
            if random.random() < 0.002:
                shock = random.gauss(0, 0.2) * price
            price = max(0.01, price * (1 + drift) + shock)
            yield (asset_id, curr_date.isoformat(), f'{price:.6f}', NOW.isoformat(), NOW.isoformat())        
            