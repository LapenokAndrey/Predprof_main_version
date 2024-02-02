import pandas
from backendAndData.yahoo_functions import *
from backendAndData.moex_functions import *
from backendAndData.base import *


@name_or_ticker
@ticker_is_compulsory()
def is_company_available(ticker: str = None, **kwargs) -> bool:
    return is_company_available_yahoo(ticker=ticker) or is_company_available_moex(ticker=ticker)


@name_or_ticker
@ticker_is_compulsory()
def get_type_of_company(ticker: str = None, **kwargs) -> str | None:
    if is_company_available_yahoo(ticker=ticker):
        return 'yahoo'

    if is_company_available_moex(ticker=ticker):
        return 'MOEX'

    return None


@name_or_ticker
@ticker_is_compulsory()
def get_stocks(ticker: str = None, start: datetime.datetime = None,
               end: datetime.datetime = None, interval: str = '1d', **kwargs) -> pandas.DataFrame | None:
    company_type = get_type_of_company(ticker=ticker)
    if company_type == 'yahoo':
        return get_stocks_yahoo(ticker=ticker, start=start, end=end, interval=interval)

    if company_type == 'MOEX':
        return get_stocks_moex(ticker=ticker, start=start, end=end, interval=interval)

    return None


@name_or_ticker
@ticker_is_compulsory()
def get_info(ticker: str = None, **kwargs) -> dict | None:
    company_type = get_type_of_company(ticker=ticker)
    if company_type == 'yahoo':
        return get_info_yahoo(ticker=ticker)

    if company_type == 'MOEX':
        return get_info_moex(ticker=ticker)

    return None


def get_name_by_ticker(ticker: str = None, **kwargs) -> dict | None:
    company_type = get_type_of_company(ticker=ticker)
    if company_type == 'yahoo':
        return get_name_by_ticker_yahoo(ticker=ticker)

    if company_type == 'MOEX':
        return get_name_by_ticker_moex(ticker=ticker)

    return None


@name_or_ticker
@ticker_is_compulsory()
def get_stocks_list(ticker: str = None, start: datetime.datetime = None,
                    end: datetime.datetime = None, interval: str = '1d', **kwargs) -> list[tuple] | None:
    company_type = get_type_of_company(ticker=ticker)
    if company_type == 'yahoo':
        return get_stocks_list_yahoo(ticker=ticker, start=start, end=end, interval=interval)

    if company_type == 'MOEX':
        return get_stocks_list_moex(ticker=ticker, start=start, end=end, interval=interval)

    return None


@name_or_ticker
def get_company_logo(company: str = None, ticker: str = None) -> str:
    """Returns link to logo of company
    (You must write ticker or name of company like attribute)"""

    if company is None:
        company = get_name_by_ticker(ticker=ticker)

    return get_company_logo_raw(company + ' company')
