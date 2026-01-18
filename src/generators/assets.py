from uuid import uuid4
from datetime import datetime 
from .constants import TICKERS_WITH_NAMES

def gen_assets():
    """Generates asset rows matching 'Asset' columns:
    (id, ticker, name, type_id, currency_id, created_at, updated_at)
    """
    NOW = datetime.now()
    assets = []

    for ticker, name in TICKERS_WITH_NAMES:
        id = str(uuid4())
        currency_id = 1 # USD
        type_id = 1 #stock
        assets.append((id, ticker, name, type_id, currency_id, NOW.isoformat(), NOW.isoformat()))

    return assets