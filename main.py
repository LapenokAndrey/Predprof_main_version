from backendAndData.mpl_functions import *
from strategy.strategy import get_strategy, BasicStrategy
import datetime
from backendAndData.flask_function import app
from backendAndData.moex_functions import *
from backendAndData.base import *
from backendAndData.functions import *


if __name__ == '__main__':
    start_time = datetime.datetime(2021, 1, 1)
    end_time = datetime.datetime(2023, 12, 1)

    # get information about company
    # get_info_yahoo(company='apple')

    # get pandas.Dataframe of stock prices of one company
    # get_stocks_yahoo(company='apple', start=start_time, end=end_time, interval='1mo')

    # get list[tuple] of stock prices of one company
    # get_close_prices_list_yahoo(company='apple', start=start_time, end=end_time, interval='1mo')

    # show graph of level of stock prices of one company
    # show_stocks_of_company_mpl('apple', start_time, end_time, '1mo')

    # show graph of levels of stick prices of plenty of companies
    # show_stocks_of_companies_mpl(['apple', 'amazon', 'microsoft'], start_time, end_time, '1mo')

    # print(get_stocks_moex(ticker='YNDX', start=start_time, end=end_time, interval='1 month'))

    app.run()
    # print(get_dataframe_of_moex_companies().columns)
    # print(get_company_logo('apple'))
