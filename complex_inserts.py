import random, math
from uuid import uuid4
from psycopg2 import connect
from datetime import datetime, timedelta
from faker import Faker

N_CUSTOMERS = 10

#DNS = 'host=localhost dbname=Enterprise user=user password=pass'
SEED = 42
fake = Faker()
Faker.seed(SEED)
random.seed(SEED)

#connection = connect(DNS)

COUNTRIES = ['US','GB','DE','FR','BR','CA','AU','IN']
RISK_PROFILES = [
    1, # conservative 
    2, # moderate
    3 # aggressive
]
BROKERAGES = [
    'ddb1a914-69d7-494e-9f73-6677ba2c222e',
    'af5aae3a-9ed0-4b64-90c7-139bea178467',
    'b5eb4b52-8dda-41e9-afb2-ebbcbe59f886'
]
ACCOUNT_TYPES = [
    1, # cash
    2, # margin
    3 # retirement
]
CURRENCIES = [
    1, #USD
    2, #EUR
    3 #BRL
]
ASSET_TYPES = [
    1, #stock
    2, #etf
    3, #bond
    4 #crypto
]
TRADE_TYPES = [
    1, #buy
    2 #sell
]
TICKERS_WITH_NAMES = [
    ("AAPL", "Apple Inc."),
    ("MSFT", "Microsoft Corporation"),
    ("AMZN", "Amazon.com Inc."),
    ("GOOG", "Alphabet Inc. (Class C)"),
    ("META", "Meta Platforms Inc."),
    ("TSLA", "Tesla Inc."),
    ("NVDA", "NVIDIA Corporation"),
    ("JPM", "JPMorgan Chase & Co."),
    ("JNJ", "Johnson & Johnson"),
    ("V", "Visa Inc."),
    ("UNH", "UnitedHealth Group Incorporated"),
    ("WMT", "Walmart Inc."),
    ("MA", "Mastercard Incorporated"),
    ("HD", "The Home Depot Inc."),
    ("PG", "Procter & Gamble Company"),
    ("BAC", "Bank of America Corporation"),
    ("DIS", "The Walt Disney Company"),
    ("XOM", "Exxon Mobil Corporation"),
    ("KO", "The Coca-Cola Company"),
    ("CVX", "Chevron Corporation"),
    ("ADBE", "Adobe Inc."),
    ("PFE", "Pfizer Inc."),
    ("CSCO", "Cisco Systems Inc."),
    ("NKE", "Nike Inc."),
    ("ORCL", "Oracle Corporation"),
    ("CRM", "Salesforce Inc."),
    ("INTC", "Intel Corporation"),
    ("T", "AT&T Inc."),
    ("PEP", "PepsiCo Inc."),
    ("ABBV", "AbbVie Inc."),
    ("MRK", "Merck & Co. Inc."),
    ("ABT", "Abbott Laboratories"),
    ("MCD", "McDonald's Corporation"),
    ("COST", "Costco Wholesale Corporation"),
    ("ACN", "Accenture plc"),
    ("TM", "Toyota Motor Corporation"),
    ("SBUX", "Starbucks Corporation"),
    ("QCOM", "Qualcomm Incorporated"),
    ("BMY", "Bristol-Myers Squibb Company"),
    ("TXN", "Texas Instruments Incorporated"),
    ("AMGN", "Amgen Inc."),
    ("HON", "Honeywell International Inc."),
    ("LIN", "Linde plc"),
    ("NEE", "NextEra Energy Inc."),
    ("MDT", "Medtronic plc"),
    ("LOW", "Lowe's Companies Inc."),
    ("LMT", "Lockheed Martin Corporation"),
    ("PM", "Philip Morris International Inc."),
    ("GS", "The Goldman Sachs Group Inc."),
    ("RTX", "RTX Corporation")
]


def gen_customers(n):
    """Yield tuples matching 'Customer' columns:
    (id,email,first_name,surname,sign_up_at,country_code,birth_date,risk_profile,created_at,updated_at)
    """
    NOW = datetime.now()
    for i in range(n):
        id = str(uuid4())
        email = f'user{i+1}@enterprise.fake'
        first_name = fake.first_name()
        surname = fake.last_name()
        sign_up_at = (NOW - timedelta(days=random.randint(0, 3650))).isoformat()
        country = random.choice(COUNTRIES)
        age = random.randint(18, 70)
        birth_date = (NOW.date() - timedelta(days=365*age)).isoformat()
        risk_profile = random.choice(RISK_PROFILES)
        yield (id, email, first_name, surname, sign_up_at, country, birth_date, risk_profile, NOW.isoformat(), NOW.isoformat())
 
    
def gen_accounts(customers):
    """Given list of customer tuples (id,...), yield account rows:
    (id, customer_id, brokerage_id, type_id, currency_id, balance, opened_at, status_id, created_at, updated_at)
    """
    NOW = datetime.now()
    for c in customers:
        customer_id = c[0]
        n_acc = random.randint(1, 3)
        for _ in range(n_acc):
            id = str(uuid4())
            brokerage_id = random.choice(BROKERAGES)
            type_id = random.choice(ACCOUNT_TYPES)
            currency_id = random.choice([*CURRENCIES, 1, 1]) # USD bias
            balance = round(math.fabs(random.gauss(5000, 20000)), 2)
            opened_at =  (NOW - timedelta(days=random.randint(0, 3650))).isoformat()
            status_id = 1 # active
            yield (id, customer_id, brokerage_id, type_id, currency_id, balance, opened_at, status_id, NOW.isoformat(), NOW.isoformat())
            
            
def gen_assets(tickers_info):
    """Yield asset rows matching Asset columns:
    (id, ticker, name, type_id, currency_id, created_at, updated_at)
    """
    NOW = datetime.now()
    for ticker, name in tickers_info:
        id = str(uuid4())
        currency_id = 1 # USD
        for type_id in ASSET_TYPES:
            yield (id, ticker, name, type_id, currency_id, NOW.isoformat(), NOW.isoformat())
            
            
def market_price_generaton():
    """Yields rows for Market_Price without 'id' column (Postgres serial).
    columns: (asset_id, price_at, price, created_at, updated_at)
    """
    pass