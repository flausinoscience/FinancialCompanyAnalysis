import random 
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
        c_id = c[0]
        c_sign_up = datetime.fromisoformat(c[4])
        c_birth_date = datetime.fromisoformat(c[6])
        c_risk_profile = c[7]

        age = int((NOW.date() - c_birth_date.date()).days / 365)
        tenure_in_days = (NOW - c_sign_up).days
        tenure_factor = max(1, tenure_in_days / 365)

        if c_risk_profile == 1:   # conservative
            n_acc = random.choices([1, 2], weights=[80, 20])[0]
            possible_types = [ACCOUNT_TYPES['cash'], ACCOUNT_TYPES['retirement']]

        elif c_risk_profile == 2: # moderate
            n_acc = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
            possible_types = list(ACCOUNT_TYPES.values())  # cash, margin, retirement

        else:                     # aggresive
            n_acc = random.choices([1, 2], weights=[65, 35])[0]
            possible_types = [ACCOUNT_TYPES['cash'], ACCOUNT_TYPES['margin']]  

        if age < 25:
            n_acc = 1
            possible_types = [ACCOUNT_TYPES['cash']]

        acc_types = random.sample(possible_types, n_acc)
        brokerage_id = random.choice(BROKERAGES)

        for acc_type in acc_types:
            acc_id = str(uuid4())
            currency_id = random.choices(list(CURRENCIES.values()), [70, 20, 10])[0]

            # --- Balance modeling ---
            base = {
                ACCOUNT_TYPES['cash']: 3000,   
                ACCOUNT_TYPES['margin']: 8000, 
                ACCOUNT_TYPES['retirement']: 15000  
            }[acc_type]
            age_factor = age / 40
            balance = max(
                100,
                random.gauss(base * age_factor * tenure_factor, base * 0.5)
            )

            opened_at = c_sign_up + timedelta(days=random.randint(0, 3))

            accounts.append((
                 acc_id,
                 c_id,
                 brokerage_id,
                 acc_type,
                 currency_id,
                 round(balance, 2),
                 opened_at.isoformat(),
                 1, # active
                 NOW.isoformat(),
                 NOW.isoformat()
             )) 

    return accounts