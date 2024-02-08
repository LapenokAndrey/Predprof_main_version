import json
import csv
import pandas
from backendAndData.base import *
import datetime
import os
from time import time
from backendAndData.online_functions import *


def get_json() -> dict:
    file = open(JSON_FILE_NAME, 'r')
    data = json.load(file)
    file.close()
    return data


def dump_json(json_data: dict) -> None:
    file = open(JSON_FILE_NAME, 'w')
    json.dump(json_data, file)
    file.close()


@name_or_ticker
@ticker_is_compulsory(default=False)
def is_company_available_domestic(ticker: str = None, **kwargs):
    return ticker in get_json()['main_data']['ticker_list']


def set_empty_companies_json_domestic() -> None:
    empty_json = {'main_data': {'company_number': 0, 'ticker_list': [], 'names_by_tickers': {}},
                  'tickers': {}}
    dump_json(empty_json)


def add_company_domestic(ticker: str, one_hour_stocks: list[pandas.DataFrame] = None,
                         one_day_stocks: list[pandas.DataFrame] = None,
                         one_month_stocks: list[pandas.DataFrame] = None) -> None:
    if one_hour_stocks is None:
        one_hour_stocks = []
    if one_day_stocks is None:
        one_day_stocks = []
    if one_month_stocks is None:
        one_month_stocks = []

    json_data = get_json()

    if ticker not in json_data['tickers']:
        json_data['tickers'][ticker] = {'1 hour': [], '1 day': [], '1 month': []}

    if ticker not in json_data['main_data']['ticker_list']:
        json_data['main_data']['company_number'] += 1
        json_data['main_data']['ticker_list'].append(ticker)
        name = get_name_by_ticker_online(ticker=ticker)
        json_data['main_data']['names_by_tickers'][ticker] = name

        info = get_info_online(ticker=ticker)
        add_company_to_db(company=name, ticker=ticker, sector=info['sector'], industry=info['industry'],
                          exchange=info['exchange'], is_available_yahoo=is_company_available_yahoo(ticker=ticker),
                          is_available_moex=is_company_available_moex(ticker=ticker))

    dump_json(json_data)

    for data in one_hour_stocks:
        add_data_domestic(ticker, data, interval='1 hour')
    for data in one_day_stocks:
        add_data_domestic(ticker, data, interval='1 day')
    for data in one_month_stocks:
        add_data_domestic(ticker, data, interval='1 month')


def add_data_domestic(ticker: str, df: pandas.DataFrame, interval: str = '1 month') -> None:
    file_data = add_df_to_csv_domestic(ticker, df, interval=interval)
    json_data = get_json()

    if ticker not in json_data['tickers']:
        add_company_domestic(ticker)
        json_data = get_json()

    json_data['tickers'][ticker][interval].append({'filename': file_data['filename'],
                                                   'path': file_data['path'],
                                                   'min_date': file_data['min_date'].__str__(),
                                                   'max_date': file_data['max_date'].__str__()})
    dump_json(json_data)
    correct_csv_files_domestic(ticker, interval=interval)


def add_df_to_csv_domestic(ticker: str, df: pandas.DataFrame, interval: str = '1 month') -> dict:
    df.sort_values(by=['Date'])

    data = convert_df_to_list_of_dicts(df)
    fields = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    if not os.path.exists(f'data/{ticker}/{interval}'):
        os.makedirs(f'./data/{ticker}/{interval}')

    min_date, max_date = data[0]['Date'], data[-1]['Date']
    _time = time()
    filename = f'data/{ticker}/{interval}/{_time}.csv'

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=DELIMITER_CSV)
        writer.writeheader()
        writer.writerows(data)

    return {'filename': f'{_time}.csv', 'path': filename, 'min_date': min_date, 'max_date': max_date, 'interval': interval}


def get_all_periods_of_company_domestic(ticker: str, interval: str = '1 month') -> list[dict] | None:
    data = get_json()

    if ticker not in data['tickers']:
        return None

    return data['tickers'][ticker][interval]


def correct_csv_files_domestic(ticker: str, interval: str = '1 month') -> None:
    data = get_json()
    if ticker not in data['tickers']:
        return None

    arrow = [None for i in range(2 * len(data['tickers'][ticker][interval]))]

    i = 0
    for row in data['tickers'][ticker][interval]:
        arrow[i] = [row['min_date'], 0, i // 2]
        arrow[i + 1] = [row['max_date'], 1, i // 2]
        i += 2

    arrow = sorted(arrow)

    level = 0
    last = None
    for i in range(len(arrow)):
        if arrow[i][1] == 0:
            level += 1

        elif arrow[i][1] == 1:
            level -= 1

        if level == 2:
            connect_csv_files(ticker, data['tickers'][ticker][interval][arrow[i][2]], last, interval=interval)
            break

        if arrow[i][1] == 0:
            last = data['tickers'][ticker][interval][arrow[i][2]]


def connect_csv_files(ticker: str, first_period: dict, second_period: dict, interval: str = '1 month') -> None:
    # print(first_period)
    # print(second_period)
    df_1 = get_df_from_csv(ticker, first_period['filename'], interval=interval).reset_index()
    df_2 = get_df_from_csv(ticker, second_period['filename'], interval=interval).reset_index()

    cond = df_2['Date'].isin(df_1['Date'])
    df_2.drop(df_2[cond].index, inplace=True)

    df = pandas.concat([df_1, df_2]).sort_values(by=['Date']).set_index('Date')

    delete_from_json(ticker, first_period, interval=interval)
    delete_from_json(ticker, second_period, interval=interval)

    delete_csv(ticker, first_period['filename'], interval=interval)
    delete_csv(ticker, second_period['filename'], interval=interval)

    add_data_domestic(ticker, df, interval=interval)


def delete_csv(ticker: str, filename: str, interval: str = '1 month') -> None:
    try:
        os.remove(f"./data/{ticker}/{interval}/{filename}")
    except:
        ...


def delete_from_json(ticker: str, period: dict, interval: str = '1 month') -> None:
    data = get_json()
    if ticker not in data['tickers']:
        return None

    if period in data['tickers'][ticker][interval]:
        data['tickers'][ticker][interval].remove(period)

    dump_json(data)


def get_df_from_csv(ticker: str, filename: str, interval: str = '1 month') -> pandas.DataFrame | None:
    try:
        df = pandas.read_csv(f'data/{ticker}/{interval}/{filename}', delimiter='|')
        return df.set_index('Date')
    except:
        return None


@name_or_ticker
@ticker_is_compulsory()
def get_stocks(ticker: str = None, start: datetime.datetime = STANDARD_START,
               end: datetime.datetime = STANDARD_START,
               interval: str = STANDARD_INTERVAL) -> pandas.DataFrame | None:
    if interval not in AVAILABLE_INTERVALS:
        return None

    json_data = get_json()

    if ticker not in json_data['tickers']:
        if not is_company_available_online(ticker=ticker):
            return None

        add_company_domestic(ticker)
        json_data = get_json()

    delta = None
    if interval == '1 month':
        delta = datetime.timedelta(weeks=5)
    elif interval == '1 day':
        if datetime.datetime.now() - end <= datetime.timedelta(days=8):
            delta = datetime.timedelta(days=8)
        else:
            delta = datetime.timedelta(days=1)
    elif interval == '1 hour':
        delta = datetime.timedelta(hours=1)

    for file in json_data['tickers'][ticker][interval]:
        if datetime.datetime.strptime(file['min_date'], '%Y-%m-%d %H:%M:%S') - delta <= start and \
                datetime.datetime.strptime(file['max_date'], '%Y-%m-%d %H:%M:%S') + delta >= end:
            df = get_df_from_csv(ticker, file['filename'], interval=interval)
            df = df.reset_index()
            df = df[start.__str__() <= df['Date']]
            df = df[df['Date'] <= end.__str__()]
            df = df.set_index('Date')
            return df
    else:
        df = get_stocks_online(ticker=ticker, start=start, end=end, interval=interval)
        df1 = df.reset_index()
        if df is None or (df1.iloc[0]['Date'] - delta).__str__() > start.__str__() or (df1.iloc[-1]['Date'] + delta).__str__() < end.__str__():
            return None

        add_data_domestic(ticker, df, interval=interval)
        return get_stocks(ticker=ticker, start=start, end=end, interval=interval)


def get_name_by_ticker(ticker: str) -> str | None:
    json_data = get_json()
    if ticker in json_data['main_data']['ticker_list']:
        return json_data['main_data']['names_by_tickers'][ticker]
    else:
        if is_company_available_online(ticker=ticker):
            add_company_domestic(ticker)
            return get_name_by_ticker(ticker)
    return None


def convert_df_to_stocks_list(df: pandas.DataFrame) -> list[tuple] | None:
    if df.empty:
        return None

    res = []
    for row in df.itertuples(name='Candle'):
        res.append(row)

    return res


def convert_df_to_list_for_graph(df: pandas.DataFrame) -> list[list] | None:
    if df.empty:
        return None

    res = []
    for row in df.itertuples():
        res.append([row[0].__str__(), row[3], row[1], row[4], row[2]])

    return res


def convert_df_to_list_for_graph_line(df: pandas.DataFrame) -> list[list] | None:
    if df.empty:
        return None

    res = []
    for row in df.itertuples():
        res.append([row[0].__str__(), (row[1] + row[4]) / 2])

    return res


def convert_df_to_close_prices_list(df: pandas.DataFrame) -> pandas.DataFrame | None:
    if df.empty:
        return None

    res = []
    for row in df.itertuples(name='Candle'):
        res.append(row[4])

    return res


one_hour_start, one_hour_end = datetime.datetime(2020, 1, 1), datetime.datetime(2024, 1, 1)
one_day_start, one_day_end = datetime.datetime(2020, 1, 1), datetime.datetime(2024, 1, 1)
one_month_start, one_month_end = datetime.datetime(2020, 1, 1), datetime.datetime(2024, 1, 1)

companies_data_example = {'main_data': {'company_number': 3, 'ticker_list': ['AAPL', 'AMZN', 'CVX']},
                          'tickers': {
                              'AAPL': {'1 hour': {(one_hour_start, one_hour_end): [[]]}, '1 day': {}, '1 month': {}},
                              'AMZN': {'1 hour': {}, '1 day': {}, '1 month': {}},
                              'CVX': {'1 hour': {}, '1 day': {}, '1 month': {}}}}
# Json, for example, (datetime.datetime, datetime): [name_of_csv_file]
# CSV, for example, [date, Open, High, Low, Close, Volume]
