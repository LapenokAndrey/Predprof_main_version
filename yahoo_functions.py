import pandas
import yfinance
from db_functions import *


"""Here are all functions, which are related to Yahoo"""


@name_or_ticker
@ticker_is_compulsory(default=False)
def is_company_available_yahoo(ticker: str = None, **kwargs) -> bool:
    """Returns True, if Yahoo is able to process this company, else False
     (You must write ticker or name of company like attribute)"""

    return not yfinance.Ticker(ticker).history().empty


def get_name_by_ticker_yahoo(ticker: str = None) -> str | None:
    """Returns name of company, using Yahoo
    (You must write ticker like attribute)"""

    if not is_company_available_yahoo(ticker=ticker):
        return None

    return get_info_yahoo(ticker=ticker)['longName']


@name_or_ticker
@ticker_is_compulsory()
def get_info_yahoo(ticker: str = None, **kwargs) -> dict | None:
    """Returns dictionary of data about company
    (You mast write ticker or name of company like attribute)"""

    return yfinance.Ticker(ticker).info


@name_or_ticker
@ticker_is_compulsory()
def get_stocks_yahoo(ticker: str = None, start: datetime.datetime = None,
                     end: datetime.datetime = None, interval: str = '1d', **kwargs) -> pandas.DataFrame | None:
    """Returns dataframe of stocks prices
    (time|Open|Close|High|Low|Volume|Dividends|Stick Splits)
    (You must write ticker or name of company like attribute)"""

    return yfinance.Ticker(ticker).history(start=start, end=end, interval=interval)


@name_or_ticker
@ticker_is_compulsory()
def get_first_time_of_company_yahoo(ticker: str = None, **kwargs) -> datetime.datetime | None:
    """It does not work now"""

    return get_stocks_yahoo(ticker=ticker, start=datetime.datetime(1600, 1, 1)).head()


@name_or_ticker
@ticker_is_compulsory()
def add_company_to_db_yahoo(ticker: str = None, **kwargs) -> None:
    """Adds company ot DB (list of all available companies)
    (You must write ticker of nam eof company like attribute)"""

    if not is_company_available_yahoo(ticker=ticker):
        return None
    info = get_info_yahoo(ticker=ticker)
    add_company_to_db(company=info['longname'], ticker=ticker, sector=info['sector'], industry=info['industry'],
                      exchange=info['exchange'], is_available_yahoo=True)


@name_or_ticker
def get_company_logo_yahoo(company: str = None, ticker: str = None) -> str:
    """Returns link to logo of company
    (You must write ticker or name of company like attribute)"""

    if company is None:
        company = get_name_by_ticker_yahoo(ticker)

    return get_company_logo(company + ' company')
