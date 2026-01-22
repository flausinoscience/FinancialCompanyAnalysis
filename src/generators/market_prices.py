import random
from datetime import datetime, timedelta
from .constants import ASSET_TYPES


ASSET_BEHAVIOR = {
    ASSET_TYPES['stock']: {'vol': 0.02,  'drift': 0.0003, 'shock_prob': 0.01,  'shock_scale': 0.08},  
    ASSET_TYPES['etf']: {'vol': 0.01,  'drift': 0.0002, 'shock_prob': 0.005, 'shock_scale': 0.04},  
    ASSET_TYPES['bond']: {'vol': 0.003, 'drift': 0.00005,'shock_prob': 0.001, 'shock_scale': 0.01},  
    ASSET_TYPES['crypto']: {'vol': 0.06,  'drift': 0.0001, 'shock_prob': 0.03,  'shock_scale': 0.25},  
}


def gen_market_prices(assets, years=5):
    """Yields rows for 'Market_Price' without 'id' column (Postgres serial).
    columns: (asset_id, price_at, price, created_at, updated_at)
    """
    NOW = datetime.now()
    start_date = NOW - timedelta(days=365 * years)

    for asset in assets:
        asset_id = asset[0]
        ticker = asset[1]
        type_id = asset[3]

        behavior = ASSET_BEHAVIOR[type_id]

        price = 20 + (abs(hash(ticker)) % 1000) * 0.1
        curr_date = start_date

        while curr_date < NOW:
            curr_date += timedelta(days=1)

            # Skip weekends for non-crypto
            if type_id != ASSET_TYPES['crypto'] and curr_date.weekday() > 4:
                continue

            drift = behavior['drift']
            vol = behavior['vol']
            shock_prob = behavior['shock_prob']
            shock_scale = behavior['shock_scale']

            daily_return = random.gauss(drift, vol)

            if random.random() < shock_prob:
                daily_return += random.gauss(0, shock_scale)

            price = max(0.5, price * (1 + daily_return))

            yield (
                asset_id,
                curr_date.isoformat(),
                f"{price:.6f}",
                NOW.isoformat(),
                NOW.isoformat()
            )
