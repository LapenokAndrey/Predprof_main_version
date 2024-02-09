import yfinance
from backendAndData.db_functions import *


"""Here are all functions, which are related to Yahoo"""


@name_or_ticker
@ticker_is_compulsory()
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

    info = yfinance.Ticker(ticker).info

    start_time = datetime.datetime(1950, 1, 1)
    end_time = datetime.datetime.now()
    df = get_stocks_yahoo(ticker=ticker,  start=start_time, end=end_time, interval='1 day').reset_index()

    info['first_available_date'] = df.iloc[0]['Date'].to_pydatetime()
    info['last_available_date'] = df.iloc[-1]['Date'].to_pydatetime()
    return info


@name_or_ticker
@ticker_is_compulsory()
@yahoo_intervals_converter
def get_stocks_yahoo(ticker: str = None, start: datetime.datetime = STANDARD_START,
                     end: datetime.datetime = STANDARD_END,
                     interval: str = STANDARD_INTERVAL, **kwargs) -> pandas.DataFrame | None:
    """Returns dataframe of stocks prices
    (time|Open|Close|High|Low|Volume|Dividends|Stick Splits)
    (You must write ticker or name of company like attribute)"""

    return yfinance.Ticker(ticker).history(start=start, end=end, interval=interval)
