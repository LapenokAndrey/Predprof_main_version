import mplfinance as mpf
from yahoo_functions import *
from db_functions import *


def get_data_of_companies(companies: list[str], start: datetime.datetime,
                          end: datetime.datetime, interval: str) -> dict:
    """Returns dictionary, where keys are names of companies and values are data about companies from Yahoo"""

    res = {}
    for company in companies:
        res[company] = get_stocks_yahoo(company=company, start=start, end=end, interval=interval)

    return res


def show_data_of_company_mpl(company: str, start: datetime.datetime,
                             end: datetime.datetime, interval: str, apds: list[pandas.DataFrame] = None,
                             volume: bool = False, type: str = 'candle', title: str = None) -> None:
    """Open interactive graph of one company"""

    df = get_stocks_yahoo(company=company, start=start, end=end, interval=interval)
    mpf.plot(df, type=type, title=company if not title else title, style='charles',
             volume=volume, addplot=([] if not apds else apds))


def show_data_of_companies_mpl(companies: list[str], start: datetime.datetime,
                           end: datetime.datetime, interval: str) -> None:
    """Open interactive graphs of companies on one plot"""

    get_stocks_yahoo(company=companies[0], start=start, end=end, interval=interval).info()
    apds = [mpf.make_addplot(get_stocks_yahoo(company=companies[i], start=start, end=end, interval=interval)['Close'], type='line') for i in range(len(companies) - 1)]
    show_data_of_company_mpl(companies[-1], start, end, interval, apds=apds, title='Companies', type='line')


def get_png_of_graph(company: str, start: datetime.datetime,
                     end: datetime.datetime, interval: str, apds: list[pandas.DataFrame] = None,
                     volume: bool = False, type: str = 'candle', title: str = None) -> None:
    """Save graph in png format in "graphs" folder (<company name>.png)"""

    filename = 'graphs/' + company + '.png'
    df = get_stocks_yahoo(company=company, start=start, end=end, interval=interval)
    mpf.plot(df, type=type, title=company if not title else title, style='charles',
             volume=volume, addplot=([] if not apds else apds), savefig=filename)


if __name__ == '__main__':
    start_time = datetime.datetime(2021, 1, 1)
    end_time = datetime.datetime(2023, 12, 1)
    array_companies = ['GM', 'F', 'CVX', 'BE']
    print(get_stocks_yahoo(company='amazon', start=start_time, end=end_time).info())
