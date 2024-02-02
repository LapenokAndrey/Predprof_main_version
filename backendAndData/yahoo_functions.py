import yfinance
from backendAndData.db_functions import *


"""Here are all functions, which are related to Yahoo"""


def is_company_available_yahoo_by_name(company: str = None, **kwargs) -> bool:
    """Returns True, if Yahoo is able to process this company, else False
     (You must write ticker or name of company like attribute)"""
    ticker = get_ticker_by_name_yahoo(company=company)
    if ticker is not None:
        return True
    return False


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

    return yfinance.Ticker(ticker).info


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


@name_or_ticker
@ticker_is_compulsory()
@yahoo_intervals_converter
def get_stocks_list_yahoo(ticker: str = None, start: datetime.datetime = STANDARD_START,
                          end: datetime.datetime = STANDARD_END,
                          interval: str = STANDARD_INTERVAL, **kwargs) -> list[tuple] | None:
    """Returns list of tuples of stock prices
    (time, open, high, low, close, volume, dividends)
    (You must write ticker or name of company like attribute)"""

    df = get_stocks_yahoo(ticker=ticker, start=start, end=end, interval=interval)
    res = []

    for row in df.itertuples(name='Candle'):
        res.append(row)

    return res


@name_or_ticker
@ticker_is_compulsory()
@yahoo_intervals_converter
def get_stocks_list_for_graph_yahoo(ticker: str = None, start: datetime.datetime = STANDARD_START,
                                    end: datetime.datetime = STANDARD_END,
                                    interval: str = STANDARD_INTERVAL, **kwargs) -> list[list] | None:
    """Returns list of lists of stock prices
    (time, low, open, close, high, volume, dividends)
    (You must write ticker or name of company like attribute)"""

    df = get_stocks_yahoo(ticker=ticker, start=start, end=end, interval=interval)
    res = []

    for row in df.itertuples():
        res.append([row[0].__str__(), row[3], row[1], row[4], row[2]])

    return res


@name_or_ticker
@ticker_is_compulsory()
@yahoo_intervals_converter
def get_stocks_list_for_graph_line_yahoo(ticker: str = None, start: datetime.datetime = STANDARD_START,
                                         end: datetime.datetime = STANDARD_END,
                                         interval: str = STANDARD_INTERVAL, **kwargs) -> list[list] | None:
    """Returns list of lists of stock prices
    (time, mean of start and close)
    (You must write ticker or name of company like attribute)"""

    df = get_stocks_yahoo(ticker=ticker, start=start, end=end, interval=interval)
    res = []

    for row in df.itertuples():
        res.append([row[0].__str__(), (row[1] + row[4]) / 2])

    return res


@name_or_ticker
@ticker_is_compulsory()
@yahoo_intervals_converter
def get_close_prices_list_yahoo(ticker: str = None, start: datetime.datetime = STANDARD_START,
                                end: datetime.datetime = STANDARD_END,
                                interval: str = STANDARD_INTERVAL, **kwargs) -> pandas.DataFrame | None:
    """Returns list of close prices of stocks
    (time, open, high, low, close, volume, dividends)
    (You must write ticker or name of company like attribute)"""

    res = get_stocks_list_yahoo(ticker=ticker, start=start, end=end, interval=interval)
    res = [price[4] for price in res]
    return res


@yahoo_intervals_converter
def get_stocks_of_companies_yahoo(companies: list[str], start: datetime.datetime,
                                  end: datetime.datetime, interval: str) -> dict:
    """Returns dictionary, where keys are names of companies and values are data about companies from Yahoo"""

    res = {}
    for company in companies:
        res[company] = get_stocks_yahoo(company=company, start=start, end=end, interval=interval)

    return res


@name_or_ticker
@ticker_is_compulsory()
def add_company_to_db_yahoo(ticker: str = None, necessary_access_level: int = 1, **kwargs) -> None:
    """Adds company ot DB (list of all available companies)
    (You must write ticker of nam eof company like attribute)"""

    if not is_company_available_yahoo(ticker=ticker):
        return None
    info = get_info_yahoo(ticker=ticker)
    add_company_to_db(company=info['longName'], ticker=ticker, sector=info['sector'], industry=info['industry'],
                      exchange=info['exchange'], is_available_yahoo=True, necessary_access_level=necessary_access_level)
