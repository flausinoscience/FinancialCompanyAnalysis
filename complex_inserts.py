import random
from uuid import uuid4
from psycopg2 import connect
from datetime import datetime, timedelta
from faker import Faker

N_CUSTOMERS = 10

DNS = 'host=localhost dbname=Enterprise user=user password=pass'
SEED = 42
NOW = datetime.now()
fake = Faker()
Faker.seed(SEED)

connection = connect(DNS)

COUNTRIES = ['US','GB','DE','FR','BR','CA','AU','IN']
RISK_PROFILES = [
    1, # conservative 
    2, # moderate
    3 # aggressive
]

def gen_customers(n):
    """Yield tuples matching 'Customer' columns:
    (id,email,first_name,surname,sign_up_at,country_code,birth_date,risk_profile,created_at,updated_at,deleted_at)
    """
    for i in range(n):
        id = str(uuid4())
        email = f'user{i+1}@enterprise.fake'
        first_name = fake.first_name()
        surname = fake.last_name()
        sign_up_at = (NOW - timedelta(days=random.randint(0, 3650))).isoformat()
        country = random.choice(COUNTRIES   )
        age = random.randint(18, 70)
        birth_date = (NOW.date() - timedelta(days=365*age)).isoformat()
        risk_profile = random.choice(RISK_PROFILES)
        yield (id, email, first_name, surname, sign_up_at, country, birth_date, risk_profile, NOW.isoformat(), NOW.isoformat())
        
for customer in gen_customers(N_CUSTOMERS): 
    print(customer)