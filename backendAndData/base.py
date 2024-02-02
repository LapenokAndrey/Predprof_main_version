import sqlite3
import requests
import wikipedia


"""Here are all functions, which do not related to Yahoo or MOEX"""


def get_ticker_by_name(company: str) -> str | None:
    """Returns ticker of company by name of this one or None, if there is not any company with given name.
    You can write not only official name, but unofficial as well"""

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


def name_or_ticker(func):
    """If there isn't ticker of company in attributes and there is name of company,
     it adds ticker to attributes by name"""

    def decorator(*args, **kwargs):
        if 'company' in kwargs and kwargs['company'] is not None and (
                'ticker' not in kwargs or kwargs['ticker'] is None):
            kwargs['ticker'] = get_ticker_by_name(kwargs['company'])

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


def get_company_logo(company_name):
    """Returns link to logo of company from wikipedia, using company name"""

    try:
        return get_wiki_log_url(company_name)

    except:
        return None


def get_wiki_log_url(page_name):
    try:
        my_page = wikipedia.page(page_name)
        image_urls = my_page.images
        logoLinks = []
        for url in image_urls:
            lower_case_url = url.lower();
            if ("commons-logo" not in lower_case_url and "-logo" not in lower_case_url and
                    "_logo" in lower_case_url and ".svg" in lower_case_url):
                logoLinks.append(url)
        return logoLinks[0]

    except:
        return None


def getExtension(url):
    for i in range(len(url) - 1, -1, -1):
        if url[i] == '.':
            return url[i:]


# All available intervals in Yahoo
INTERVALS_YAHOO = {'15 minutes': '15m', '30 minutes': '30m', '1 hour': '1h', '1 day': '1d', '5 days': '5d',
                   '1 month': '1mo', '3 months': '3mo'}

# It is obligatory for sqlite
connection = sqlite3.connect('data/DB_finance.db', check_same_thread=False)
cursor = connection.cursor()

USER_COLUMNS = ['id', 'email', 'password', 'access_level']
COMPANY_COLUMNS = ['id', 'name', 'ticker', 'sector', 'industry', 'exchange',
                   'is_available_yahoo', 'necessary_access_level']
