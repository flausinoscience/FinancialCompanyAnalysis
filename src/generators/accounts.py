import random, math
from uuid import uuid4
from datetime import datetime, timedelta
from .constants import ACCOUNT_TYPES, BROKERAGES, CURRENCIES

def gen_accounts(customers):
    """Given a list of customers, generates account rows (1-3) per customer:
    (id, customer_id, brokerage_id, type_id, currency_id, balance, opened_at, status_id, created_at, updated_at)
    """
    NOW = datetime.now()
    accounts = []

    for c in customers:
        # c is a tuple
        customer_id = c[0]
        customer_sign_up_at = datetime.fromisoformat(c[4])
        n_acc = random.randint(1, 3)
        acc_types = random.sample(ACCOUNT_TYPES, n_acc)
        for acc_type in acc_types:
            id = str(uuid4())
            brokerage_id = random.choice(BROKERAGES)
            type_id = acc_type
            currency_id = random.choice([*CURRENCIES, 1, 1]) # USD bias
            balance = round(math.fabs(random.gauss(5000, 20000)), 2)
            opened_at =  (customer_sign_up_at + timedelta(days=random.randint(0, 3))).isoformat()
            status_id = 1 # active
            accounts.append((id, customer_id, brokerage_id, type_id, currency_id, balance, opened_at, status_id, NOW.isoformat(), NOW.isoformat()))

    return accounts