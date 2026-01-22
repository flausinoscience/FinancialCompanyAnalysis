from pathlib import Path
from ..generators import (
    gen_customers,
    gen_accounts,
    gen_assets,
    gen_market_prices
)
from ..db.connection import get_engine
from ..db.ingestion import batch_insert, run_sql_file, copy_stream

BASE_DIR = Path(__file__).resolve().parents[2]  # project root
SQL_PATH = BASE_DIR / 'src/generators' / 'base_inserts.sql'
N_CUSTOMERS = 100
YEARS_OF_MARKET_PRICES = 7

def run():
    engine = get_engine()

    run_sql_file(engine, SQL_PATH)

    print('----------------->\nGenerating customers...')
    customers = gen_customers(N_CUSTOMERS)
    batch_insert(engine, 'Customer', (
                'id','email','first_name','surname','sign_up_at','country_code',
                'birth_date','risk_profile','created_at','updated_at'
                ), customers)
        
        
    print('----------------->\nGenerating accounts...')
    accounts = gen_accounts(customers)
    batch_insert(engine, 'Account', (
                'id', 'customer_id', 'brokerage_id', 'type_id', 'currency_id',
                'balance', 'opened_at', 'status_id', 'created_at', 'updated_at'
                ), accounts)
        

    print('----------------->\nGenerating assets...')
    assets = gen_assets()
    batch_insert(engine, 'Asset', (
                'id', 'ticker', 'name', 'type_id', 'currency_id',
                'created_at', 'updated_at'
                ), assets)
    
    
    print('----------------->\nGenerating market_prices...')
    market_prices = gen_market_prices(assets, YEARS_OF_MARKET_PRICES)
    copy_stream(engine, 'Market_Price', (
                'asset_id', 'price_at', 'price', 'created_at', 'updated_at'
                ), market_prices)


if __name__ == '__main__':
    run() 