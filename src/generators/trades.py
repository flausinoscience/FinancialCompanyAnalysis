import random
from uuid import uuid4
from datetime import datetime, timedelta, time
from collections import defaultdict
from .constants import RISK_PROFILES, ACCOUNT_TYPES, ASSET_TYPES

BUY = 1
SELL = 2

def assets_by_type(assets):
    asset_by_type = defaultdict(list)

    for asset in assets:
        asset_id = asset[0]
        asset_type = asset[3]

        asset_by_type[asset_type].append(asset_id)

    return asset_by_type


def pick_asset_with_bias(assets_id_by_type, risk_profile_id):
    if risk_profile_id == RISK_PROFILES['conservative']:
        weights = {
            ASSET_TYPES['bond']: 50,
            ASSET_TYPES['etf']: 35,
            ASSET_TYPES['stock']: 14,
            ASSET_TYPES['crypto']: 1
        }

    elif risk_profile_id == RISK_PROFILES['moderate']:
        weights = {
            ASSET_TYPES['bond']: 15,
            ASSET_TYPES['etf']: 40,
            ASSET_TYPES['stock']: 40, 
            ASSET_TYPES['crypto']: 5
        }

    else:
        weights = {
            ASSET_TYPES['bond']: 2,
            ASSET_TYPES['etf']: 18,
            ASSET_TYPES['stock']: 50,
            ASSET_TYPES['crypto']: 30
        }

    preferred_asset_type = random.choices(
        list(weights.keys()),
        list(weights.values())
    )[0]

    return random.choice(assets_id_by_type[preferred_asset_type])


def gen_trades(customers, accounts, assets, asset_price_history):
    NOW = datetime.now()

    assets_id_by_type = assets_by_type(assets)

    for acc in accounts:
        acc_id = acc[0]
        customer_id = acc[1]
        acc_type = acc[3]
        opened_at = datetime.fromisoformat(acc[6])

        customer = next(c for c in customers if c[0] == customer_id)
        risk_profile_id = customer[7]

        # --- trading intensity ---
        if risk_profile_id == RISK_PROFILES['conservative']:
            trades_per_month = random.uniform(0.5, 2)
        elif risk_profile_id == RISK_PROFILES['moderate']:
            trades_per_month = random.uniform(2, 6)
        else:
            trades_per_month = random.uniform(6, 20)

        # account type modifier
        if acc_type == ACCOUNT_TYPES['margin']:
            trades_per_month *= 1.5
        elif acc_type == ACCOUNT_TYPES['retirement']: 
            trades_per_month *= 0.3

        days_active = (NOW - opened_at).days
        expected_trades = int(days_active / 30 * trades_per_month)

        for _ in range(expected_trades):

            trade_day = opened_at + timedelta(days=random.randint(1, days_active))
            if trade_day.weekday() > 4:
                continue

            traded_at = datetime.combine(
                trade_day.date(),
                time(random.randint(10, 15), random.randint(0, 59))
            )

            # --- asset choice bias ---
            asset_id = pick_asset_with_bias(assets_id_by_type, risk_profile_id)

            prices = asset_price_history.get(asset_id)
            if not prices:
                continue

            price = prices.get(traded_at.date())
            if not price:
                continue

            price *= random.uniform(0.998, 1.002)  # slippage

            # --- buy/sell behavior ---
            if risk_profile_id == RISK_PROFILES['conservative']:
                trade_type = random.choices([BUY, SELL], [85, 15])[0]

            elif risk_profile_id == RISK_PROFILES['moderate']:
                trade_type = random.choices([BUY, SELL], [65, 35])[0]

            else:
                trade_type = random.choice([BUY, SELL])

            quantity = round(random.uniform(1, 50), 4)
            commission = round(price * quantity * 0.001, 4)

            yield (
                str(uuid4()),
                asset_id,
                acc_id,
                trade_type,
                quantity,
                round(price, 6),
                traded_at.isoformat(),
                commission,
                False,
                None,
                NOW.isoformat(),
                NOW.isoformat()
            )
