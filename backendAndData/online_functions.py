from backendAndData.yahoo_functions import *
from backendAndData.moex_functions import *
from backendAndData.base import *


def yahoo_or_moex(yahoo_func, moex_func):
    def wrapper(func):
        def decorator(*args, **kwargs):
            company_type = get_type_of_company_online(ticker=kwargs['ticker'])
            if company_type == 'yahoo':
                return yahoo_func(**kwargs)

            if company_type == 'MOEX':
                return moex_func(**kwargs)

            return None
        return decorator
    return wrapper


@name_or_ticker
@ticker_is_compulsory()
def is_company_available_online(ticker: str = None, **kwargs) -> bool:
    return is_company_available_yahoo(ticker=ticker) or is_company_available_moex(ticker=ticker)


@name_or_ticker
@ticker_is_compulsory()
def get_type_of_company_online(ticker: str = None, **kwargs) -> str | None:
    if is_company_available_yahoo(ticker=ticker):
        return 'yahoo'

    if is_company_available_moex(ticker=ticker):
        return 'MOEX'

    return None


@name_or_ticker
@ticker_is_compulsory()
@yahoo_or_moex(get_stocks_yahoo, get_stocks_moex)
def get_stocks_online(ticker: str = None, start: datetime.datetime = STANDARD_START,
                      end: datetime.datetime = STANDARD_END,
                      interval: str = STANDARD_INTERVAL, **kwargs) -> pandas.DataFrame | None: ...


@name_or_ticker
@ticker_is_compulsory()
@yahoo_or_moex(get_info_yahoo, get_info_moex)
def get_info_online(ticker: str = None, **kwargs) -> dict | None: ...


@ticker_is_compulsory()
@yahoo_or_moex(get_name_by_ticker_yahoo, get_name_by_ticker_moex)
def get_name_by_ticker_online(ticker: str = None) -> dict | None: ...


@name_or_ticker
def get_company_logo_online(company: str = None, ticker: str = None) -> str:
    """Returns link to logo of company
    (You must write ticker or name of company like attribute)"""
    if company is None:
        company = get_name_by_ticker_online(ticker=ticker)

    return get_company_logo_raw(company + ' company')


@name_or_ticker
def get_description_online(company: str = None, ticker: str = None) -> str:
    if company is None:
        company = get_name_by_ticker_online(ticker=ticker)

    try:
        return wikipedia.summary(company + ' company', sentences=3)
    except:
        return 'No data'
