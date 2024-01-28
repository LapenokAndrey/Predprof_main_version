import datetime
from base import *


"""Here are all functions for work with DB"""


def add_company_to_db(company: str = None, ticker: str = None, sector: str = None, industry: str = None,
                      exchange: str = None,
                      is_available_yahoo: bool = False, is_available_moex=False,
                      start_of_available_period: datetime.datetime = None,
                      end_of_available_period: datetime.datetime = None) -> None:
    """Add new company to DB to table where are all "available" companies"""

    cursor.execute("""
        INSERT INTO Companies (name, ticker, sector, industry, exchange, is_available_yahoo, is_available_moex, start_of_available_period, end_of_available_period)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (company, ticker, sector, exchange, industry, is_available_yahoo, is_available_moex,
              start_of_available_period, end_of_available_period))
    connection.commit()
