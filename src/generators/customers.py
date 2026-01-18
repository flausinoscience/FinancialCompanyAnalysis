import random
from uuid import uuid4
from datetime import datetime, timedelta
from faker import Faker
from .constants import COUNTRIES, RISK_PROFILES

fake = Faker()

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
        sign_up_at = (NOW - timedelta(days=random.randint(0, 365 * 5))).isoformat()
        country = random.choice(COUNTRIES)
        age = random.randint(18, 70)
        birth_date = (NOW.date() - timedelta(days=365*age)).isoformat()
        risk_profile = random.choice(RISK_PROFILES)
        customers.append((id, email, first_name, surname, sign_up_at, country, birth_date, risk_profile, NOW.isoformat(), NOW.isoformat()))

    return customers