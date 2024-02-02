from backendAndData.yahoo_functions import *
from backendAndData.moex_functions import *
import mplfinance as mpf
import datetime


def show_stocks_of_company_mpl(company: str, start: datetime.datetime,
                               end: datetime.datetime, interval: str, apds: list[pandas.DataFrame] = None,
                               volume: bool = False, type: str = 'candle', title: str = None) -> None:
    """Open interactive graph of one company"""

    df = get_stocks_yahoo(company=company, start=start, end=end, interval=interval)
    mpf.plot(df, type=type, title=company if not title else title, style='charles',
             volume=volume, addplot=([] if not apds else apds))


def show_stocks_of_companies_mpl(companies: list[str], start: datetime.datetime,
                                 end: datetime.datetime, interval: str) -> None:
    """Open interactive graphs of companies on one plot"""

    apds = [mpf.make_addplot(get_stocks_yahoo(company=companies[i], start=start, end=end, interval=interval)['Close'], type='line') for i in range(len(companies) - 1)]
    show_stocks_of_company_mpl(companies[-1], start, end, interval, apds=apds, title='Companies', type='line')


def get_png_of_graph(company: str, start: datetime.datetime,
                     end: datetime.datetime, interval: str, apds: list[pandas.DataFrame] = None,
                     volume: bool = False, type: str = 'candle', title: str = None) -> None:
    """Save graph in png format in "graphs" folder (<company name>.png)"""

    filename = 'graphs/' + company + '.png'
    df = get_stocks_yahoo(company=company, start=start, end=end, interval=interval)
    mpf.plot(df, type=type, title=company if not title else title, style='charles',
             volume=volume, addplot=([] if not apds else apds), savefig=filename)
