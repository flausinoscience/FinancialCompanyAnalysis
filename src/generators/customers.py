import random
from uuid import uuid4
from datetime import datetime, timedelta
from faker import Faker
from .constants import COUNTRY_WEIGHTS, RISK_PROFILES

fake = Faker()

def pick_country():
    return random.choices(
        list(COUNTRY_WEIGHTS.keys()),
        weights=COUNTRY_WEIGHTS.values()
    )[0]
    
    
def gen_signup_date(age):
    now = datetime.now()

    if age < 30:
        days_ago = random.randint(0, 365 * 2)   # young users join recently
    elif age < 50:
        days_ago = random.randint(0, 365 * 4) # moderate
    else:
        days_ago = random.randint(365, 365 * 7) # joined a long time ago on the platform

    return now - timedelta(days=days_ago)


def assign_risk_profile(age):
    if age < 30:
        return random.choices(list(RISK_PROFILES.values()), weights=[0.1, 0.3, 0.6])[0]
    elif age < 50:
        return random.choices(list(RISK_PROFILES.values()), weights=[0.2, 0.6, 0.2])[0]
    else:
        return random.choices(list(RISK_PROFILES.values()), weights=[0.6, 0.35, 0.05])[0]


def gen_age():
    age = int(random.gauss(38, 12))  # mean=38, std=12
    return max(18, min(age, 75))


def gen_customers(n):
    """Generates tuples matching 'Customer' columns:
    (id,email,first_name,surname,sign_up_at,country_code,birth_date,risk_profile,created_at,updated_at)
    """
    NOW = datetime.now()
    customers = []

    for i in range(n):
        id = str(uuid4())
        email = f'user{i+1}@enterprise.fake'
        first_name = fake.first_name()
        surname = fake.last_name()

        age = gen_age()
        birth_date = (NOW.date() - timedelta(days=age*365))
        risk_profile = assign_risk_profile(age)
        sign_up_at = gen_signup_date(age)
        country = pick_country()

        customers.append((
            id,
            email,
            first_name,
            surname,
            sign_up_at.isoformat(),
            country,
            birth_date.isoformat(),
            risk_profile,
            NOW.isoformat(),
            NOW.isoformat()
        ))

    return customers
