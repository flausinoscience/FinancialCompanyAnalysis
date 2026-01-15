import io, csv, random, math
from uuid import uuid4
from psycopg2 import connect
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
from faker import Faker

N_CUSTOMERS = 10
N_MARKET_PRICES = 10

DNS = 'host=localhost dbname=Enterprise user=user password=pass'
fake = Faker()
Faker.seed()
random.seed()

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
        sign_up_at = (NOW - timedelta(days=random.randint(0, 365 * 10))).isoformat()
        country = random.choice(COUNTRIES)
        age = random.randint(18, 70)
        birth_date = (NOW.date() - timedelta(days=365*age)).isoformat()
        risk_profile = random.choice(RISK_PROFILES)
        customers.append((id, email, first_name, surname, sign_up_at, country, birth_date, risk_profile, NOW.isoformat(), NOW.isoformat()))

    return customers
    

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
            
            
def gen_market_prices(assets, n):
    """Yields rows for 'Market_Price' without 'id' column (Postgres serial).
    columns: (asset_id, price_at, price, created_at, updated_at)
    """
    NOW = datetime.now()

    total_assets = len(TICKERS_WITH_NAMES)
    rows_per_asset = max(10, n // total_assets)
    
    # ~3 years of backfilled price history.
    start_date = (NOW - timedelta(days=365*3))
    
    for a in assets:
        asset_id = a[0]
        ticker = a[1]
        price = 20.0 + (abs(hash(ticker)) % 1000) * 0.1
        curr_date = start_date
        for _ in range(rows_per_asset):
            curr_date += timedelta(days=1)
            # no weekends allowed
            if curr_date.weekday() > 4:
                continue
            # random-walk with occasional shock
            drift = random.gauss(0, 0.001)
            shock = 0.0
            if random.random() < 0.002:
                shock = random.gauss(0, 0.2) * price
            price = max(0.01, price * (1 + drift) + shock)
            yield (asset_id, curr_date.isoformat(), f'{price:.6f}', NOW.isoformat(), NOW.isoformat())        
            

# ---------- DB helpers ----------
def batch_insert(conn, table, columns, rows):
    cur = conn.cursor()
    cols = ', '.join(f'"{col}"' for col in columns)
    insert_command = f'INSERT INTO public."{table}" ({cols}) VALUES %s'
    batch = []

    for row in rows:
        batch.append(row)
        if len(batch) >= 2000:
            execute_values(cur, insert_command, batch, template=None)
            conn.commit()
            batch.clear()
    
    if batch:
        execute_values(cur, insert_command, batch, template=None)
        conn.commit()
        
    cur.close()


def copy_stream(conn, table, columns, rows):
    """COPY FROM STDIN streaming of CSV-formatted rows using 
    csv.writer into StringIO buffer."""
    cur = conn.cursor()
    cols = ', '.join(f'"{col}"' for col in columns)
    copy_command = f'COPY public."{table}"({cols}) FROM STDIN WITH CSV'
    buf = io.StringIO()
    writer = csv.writer(buf)
    rows_in_buf = 0
    
    for row in rows:
        writer.writerow(row)
        rows_in_buf += 1
        if rows_in_buf >= 20_000:
            buf.seek(0)
            try:
                cur.copy_expert(copy_command, buf)
                conn.commit()
            except Exception as _:
                conn.rollback()
                raise
            buf = io.StringIO()
            writer = csv.writer(buf)
            rows_in_buf = 0
    
    if rows_in_buf:
        buf.seek(0)
        try:
            cur.copy_expert(copy_command, buf)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
    
    cur.close()
        

if __name__ == '__main__':
    conn = connect(DNS)

    try:
        print('----------------->\nGenerating customers...')
        customers = gen_customers(N_CUSTOMERS)
        batch_insert(conn, 'Customer', (
                    'id','email','first_name','surname','sign_up_at','country_code',
                    'birth_date','risk_profile','created_at','updated_at'
                    ), customers)
        
        
        print('----------------->\nGenerating accounts...')
        accounts = gen_accounts(customers)
        batch_insert(conn, 'Account', (
                    'id', 'customer_id', 'brokerage_id', 'type_id', 'currency_id',
                    'balance', 'opened_at', 'status_id', 'created_at', 'updated_at'
                    ), accounts)
        

        print('----------------->\nGenerating assets...')
        assets = gen_assets()
        batch_insert(conn, 'Asset', (
                    'id', 'ticker', 'name', 'type_id', 'currency_id',
                    'created_at', 'updated_at'
                    ), assets)


        # Stream Market_Price via COPY
        print('----------------->\nStreaming market prices via COPY...')
        market_prices = gen_market_prices(assets, N_MARKET_PRICES)
        copy_stream(conn, 'Market_Price', (
                    'asset_id', 'price_at', 'price', 'created_at', 'updated_at'
                    ), market_prices)
    
    finally:
        conn.close()