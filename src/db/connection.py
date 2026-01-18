import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DB = os.getenv('DB_NAME')

# postgresql+psycopg2://username:password@host:port/database
CONN_STR = f'postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DB}'

_engine = create_engine(CONN_STR)


def q(sql):
    """Query the database with the sql provided. Returns a pandas DataFrame"""
    return pd.read_sql(sql, _engine)


def get_engine():
    return _engine