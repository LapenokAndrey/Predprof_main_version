from backendAndData.base import *
import random


"""Here are all functions for work with DB"""


def if_email_exists_only(func):
    def decorator(*args, **kwargs):
        if 'email' in kwargs and cursor.execute("""SELECT * FROM users WHERE email = ?""", (kwargs['email'],)).fetchone():
            return func(*args, **kwargs)

        return None

    return decorator


def if_ticker_exists_only(func):
    """If there isn't ticker of company in attributes and there is name of company,
     it adds ticker to attributes by name"""

    def decorator(*args, **kwargs):
        if 'ticker' in kwargs and cursor.execute("""SELECT * FROM companies WHERE ticker = ?""", (kwargs['ticker'],)).fetchone():
            return func(*args, **kwargs)

        return None

    return decorator


def add_company_to_db(company: str = None, ticker: str = None, sector: str = None, industry: str = None,
                      exchange: str = None, is_available_yahoo: bool = False, is_available_moex: bool = False,
                      necessary_access_level: int = 0, first_available_date: datetime.datetime = None,
                      last_available_date: datetime.datetime = None) -> None:
    """Add new company to DB to table where are all "available" companies"""
    try:
        description = wikipedia.summary(company + ' company', sentences=3)
    except:
        description = 'No data'

    cursor.execute("""
        INSERT INTO Companies (name, ticker, sector, industry, exchange, is_available_yahoo, is_available_moex, necessary_access_level, logo, description, first_available_date, last_available_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (company, ticker, sector, industry, exchange, is_available_yahoo, is_available_moex,
              necessary_access_level, get_company_logo_raw(company + 'company'), description,
              first_available_date, last_available_date))
    connection.commit()


@if_ticker_exists_only
def get_company(ticker: str = None) -> list:
    res = cursor.execute("""SELECT * FROM companies WHERE ticker = ?""", (ticker,)).fetchone()
    return res


@if_ticker_exists_only
def get_description_db(ticker: str = None):
    res = cursor.execute("""SELECT description FROM companies WHERE ticker = ?""", (ticker,)).fetchone()
    if res is None:
        return None
    return res[0]


@if_ticker_exists_only
def get_company_dict(ticker: str = None) -> dict:
    user = get_company(ticker=ticker)
    res = {COMPANY_COLUMNS[i]: user[i] for i in range(len(COMPANY_COLUMNS))}
    return res


@if_ticker_exists_only
def change_company_necessary_access_level(ticker: str = None, new_necessary_access_level: str = None) -> None:
    cursor.execute("""UPDATE users SET password = ? WHERE ticker = ?""", (new_necessary_access_level, ticker))
    connection.commit()


def get_names_available_companies(n: int = 10) -> list[str]:
    res = cursor.execute("""
        SELECT name FROM companies""").fetchall()
    random.shuffle(res)
    res = res[:n]
    return [company[0] for company in res]


def is_user(email: str = None, password: str = None) -> bool:
    user = cursor.execute("""
        SELECT * FROM users WHERE email = ? AND password = ?""", (email, password)).fetchone()
    if user:
        return True
    return False


def add_user_to_db(email: str = None, password: str = None, access_level: int = 0) -> None:
    cursor.execute("""
            INSERT INTO users (email, password, access_level)
            VALUES (?, ?, ?);
            """, (email, password, access_level))
    connection.commit()


@if_email_exists_only
def get_user(email: str = None) -> list:
    res = cursor.execute("""SELECT * FROM users WHERE email = ?""", (email,)).fetchone()
    return res


@if_email_exists_only
def get_user_dict(email: str = None) -> dict:
    user = get_user(email=email)
    res = {USER_COLUMNS[i]: user[i] for i in range(len(USER_COLUMNS))}
    return res


@if_email_exists_only
def change_user_access_level(email: str = None, new_access_level: int = 1) -> None:
    cursor.execute("""UPDATE users SET access_level = ? WHERE email = ?""", (new_access_level, email))
    connection.commit()


@if_email_exists_only
def change_user_email(email: str = None, new_email: str = None) -> None:
    cursor.execute("""UPDATE users SET email = ? WHERE email = ?""", (new_email, email))
    connection.commit()


@if_email_exists_only
def change_user_password(email: str = None, new_password: str = None) -> None:
    cursor.execute("""UPDATE users SET password = ? WHERE email = ?""", (new_password, email))
    connection.commit()


@name_or_ticker
def get_logo_from_db(ticker: str = None, **kwargs) -> str:
    return cursor.execute("""SELECT logo FROM companies WHERE ticker = ?""", (ticker,)).fetchone()[0]


def is_email(email: str) -> bool:
    user = cursor.execute("""
            SELECT * FROM users WHERE email = ?""", (email,)).fetchone()

    if user:
        return True
    return False

