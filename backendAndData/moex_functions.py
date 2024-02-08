import pandas as pd
from backendAndData.db_functions import *


@name_or_ticker
@ticker_is_compulsory()
def get_info_moex(ticker: str = None, **kwargs) -> dict | None:
    df = get_dataframe_of_moex_companies()
    df = df[df['SECID'] == ticker]
    data = {'ticker': df.iloc[0]['SECID'], 'longName': df.iloc[0]['SHORTNAME'],
            'exchange': 'MOEX', 'sector': None, 'industry': None}
    return data


def get_name_by_ticker_moex(ticker: str = None) -> str | None:
    if not is_company_available_moex(ticker=ticker):
        return None

    return get_info_moex(ticker=ticker)['longName']


@name_or_ticker
@ticker_is_compulsory()
@moex_intervals_converter
def get_stocks_moex_raw(ticker: str = None, start: datetime.datetime = STANDARD_START,
                        end: datetime.datetime = STANDARD_END,
                        interval: str = STANDARD_INTERVAL, **kwargs) -> pandas.DataFrame | None:
    j = requests.get(
        f'http://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json?from={start.__str__()[:10]}&till={end.__str__()[:10]}&interval={interval}').json()
    data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
    frame = pd.DataFrame(data)

    return frame


def convert_moex_df_to_yahoo_format(df: pandas.DataFrame = None) -> pandas.DataFrame | None:
    if df is None:
        return None

    dates, opens, closes, highs, lows, volumes = [], [], [], [], [], []
    for row in df.itertuples():
        dates.append(datetime.datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S'))
        opens.append(row[1])
        closes.append(row[2])
        highs.append(row[3])
        lows.append(row[4])
        volumes.append(row[6])

    res = pandas.DataFrame({'Date': dates, 'Open': opens, 'High': highs, 'Low': lows,
                            'Close': closes, 'Volume': volumes})
    return res.set_index('Date')


@name_or_ticker
@ticker_is_compulsory()
@moex_intervals_converter
def get_stocks_moex(ticker: str = None, start: datetime.datetime = STANDARD_START,
                    end: datetime.datetime = STANDARD_END,
                    interval: str = STANDARD_INTERVAL, **kwargs) -> pandas.DataFrame | None:
    return convert_moex_df_to_yahoo_format(df=get_stocks_moex_raw(ticker=ticker,
                                                                  start=start, end=end, interval=interval))


@name_or_ticker
@ticker_is_compulsory(default=False)
def is_company_available_moex(ticker: str = None, **kwargs) -> bool:
    """Returns True, if Yahoo is able to process this company, else False
     (You must write ticker or name of company like attribute)"""

    return ticker in get_dataframe_of_moex_companies()['SECID'].values


@name_or_ticker
@ticker_is_compulsory()
def add_company_to_db_moex(ticker: str = None, necessary_access_level: int = 1, **kwargs) -> None:
    """Adds company ot DB (list of all available companies)
    (You must write ticker of nam eof company like attribute)"""

    if not is_company_available_moex(ticker=ticker):
        return None

    info = get_info_moex(ticker=ticker)
    add_company_to_db(company=info['longName'], ticker=ticker,
                      exchange='MOEX', is_available_moex=True, necessary_access_level=necessary_access_level)
