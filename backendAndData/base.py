import sqlite3
import requests
import wikipedia
from moexalgo import Market
import pandas
import difflib
from transliterate import translit
import datetime


"""Here are all functions, which do not related to Yahoo or MOEX"""


def get_dataframe_of_moex_companies() -> pandas.DataFrame:
    return pandas.DataFrame(stocks.tickers())


def get_ticker_by_name_yahoo(company: str = None) -> str | None:
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company, "quotes_count": 1}
    res = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
    data = res.json()

    try:
        company_code = data['quotes'][0]['symbol']
    except:
        return None

    return company_code


def get_ticker_by_name_moex(company: str = None) -> str | None:
    company_en = translit(company, language_code='ru', reversed=True)
    company_ru = translit(company, language_code='ru')

    companies = get_dataframe_of_moex_companies()[['SHORTNAME', 'SECID']]
    company_names_ru = difflib.get_close_matches(company_ru, companies['SHORTNAME'], cutoff=.5)
    company_names_en = difflib.get_close_matches(company_en, companies['SHORTNAME'], cutoff=.5)

    if company_names_ru:
        company_name = company_names_ru[0]
    elif company_names_en:
        company_name = company_names_en[0]
    else:
        return None

    return companies[companies['SHORTNAME'] == company_name].iloc[0]['SECID']


def get_ticker_by_name(company: str) -> str | None:
    """Returns ticker of company by name of this one or None, if there is not any company with given name.
    You can write not only official name, but unofficial as well"""

    ticker = get_ticker_by_name_yahoo(company=company)
    if ticker is not None:
        return ticker

    ticker = get_ticker_by_name_moex(company=company)
    if ticker is not None:
        return ticker


def name_or_ticker(func):
    """If there isn't ticker of company in attributes and there is name of company,
     it adds ticker to attributes by name"""

    def decorator(*args, **kwargs):
        if 'company' in kwargs and kwargs['company'] is not None and (
                'ticker' not in kwargs or kwargs['ticker'] is None):
            try:
                kwargs['ticker'] = get_ticker_by_name(kwargs['company'])
            except:
                return None

        return func(*args, **kwargs)

    return decorator


def ticker_is_compulsory(default=None):
    """If there isn't ticker in attributes, it returns default value"""

    def wrapper(func):
        def decorator(*args, **kwargs):
            if 'ticker' not in kwargs or kwargs['ticker'] is None:
                return default
            return func(*args, **kwargs)
        return decorator
    return wrapper


def get_company_logo_raw(company_name):
    """Returns link to logo of company from wikipedia, using company name"""

    try:
        return get_wiki_log_url(company_name)

    except:
        return None


def get_wiki_log_url(page_name):
    try:
        my_page = wikipedia.page(page_name)
        image_urls = my_page.images
        logo_links = []
        for url in image_urls:
            lower_case_url = url.lower();
            if ("commons-logo" not in lower_case_url and "-logo" not in lower_case_url and
                    "_logo" in lower_case_url and ".svg" in lower_case_url):
                logo_links.append(url)
        return logo_links[-1]

    except:
        return None


def get_extension(url):
    for i in range(len(url) - 1, -1, -1):
        if url[i] == '.':
            return url[i:]


def moex_intervals_converter(func):
    def decorator(*args, **kwargs):
        if 'interval' in kwargs and kwargs['interval'] in INTERVALS_MOEX:
            kwargs['interval'] = INTERVALS_MOEX[kwargs['interval']]

        if 'interval' not in kwargs:
            kwargs['interval'] = INTERVALS_MOEX[STANDARD_INTERVAL]

        return func(*args, **kwargs)

    return decorator


def yahoo_intervals_converter(func):
    def decorator(*args, **kwargs):
        if 'interval' in kwargs and kwargs['interval'] in INTERVALS_YAHOO:
            kwargs['interval'] = INTERVALS_YAHOO[kwargs['interval']]

        if 'interval' not in kwargs:
            kwargs['interval'] = INTERVALS_YAHOO[STANDARD_INTERVAL]

        return func(*args, **kwargs)

    return decorator


def convert_df_to_list_of_dicts(df: pandas.DataFrame) -> list[dict]:
    res = [{} for i in range(len(df))]
    for i, row in enumerate(df.itertuples()):
        res[i] = {'Date': row[0], 'Open': row[1], 'High': row[2], 'Low': row[3], 'Close': row[4], 'Volume': row[5]}
        if len(row[0].__str__()) == len('2020-12-12 12:12:12-00:00'):
            res[i]['Date'] = datetime.datetime.strptime(row[0].__str__()[:19], '%Y-%m-%d %H:%M:%S')
        if len(row[0].__str__()) == len('2020-12-12'):
            res[i]['Date'] = datetime.datetime.strptime(row[0].__str__() + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
    return res


# All available intervals in Yahoo
INTERVALS_YAHOO = {'15 minutes': '15m', '30 minutes': '30m', '1 hour': '1h', '1 day': '1d', '5 days': '5d',
                   '1 month': '1mo', '3 months': '3mo'}
INTERVALS_MOEX = {'1 minute': 1, '10 minutes': 10, '1 hour': 60, '1 day': 24, '1 week': 7, '1 month': 31, '1 year': 4}
AVAILABLE_INTERVALS = ['1 hour', '1 day', '1 month']

# It is obligatory for sqlite
connection = sqlite3.connect('data/DB_finance.db', check_same_thread=False)
cursor = connection.cursor()

USER_COLUMNS = ['id', 'email', 'password', 'access_level']
COMPANY_COLUMNS = ['id', 'name', 'ticker', 'sector', 'industry', 'exchange',
                   'is_available_yahoo', 'necessary_access_level']

stocks = Market("shares/TQBR")

STANDARD_START = datetime.datetime(2022, 1, 1)
STANDARD_END = datetime.datetime(2024, 1, 1)
STANDARD_INTERVAL = '1 month'

JSON_FILE_NAME = 'data/companies.json'

DELIMITER_CSV = '|'
