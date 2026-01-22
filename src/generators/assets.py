from uuid import uuid4
from datetime import datetime
from .constants import ASSETS, ASSET_TYPES, CURRENCIES


def gen_assets():
    """Generates asset rows matching 'Asset' columns:
    (id, ticker, name, type_id, currency_id, created_at, updated_at)
    """
    NOW = datetime.now()
    assets = []

    for ticker, name, asset_type, currency in ASSETS:
        asset_id = str(uuid4())

        type_id = ASSET_TYPES[asset_type]
        currency_id = CURRENCIES[currency]

        assets.append((
            asset_id,
            ticker,
            name,
            type_id,
            currency_id,
            NOW.isoformat(),
            NOW.isoformat()
        ))

    return assets
