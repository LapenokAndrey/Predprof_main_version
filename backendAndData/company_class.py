import pandas

from backendAndData.data_functions import *


class Company:
    all_formats = ['close_prices_list', 'list_for_graph_line', 'list_for_graph', 'stocks_list']

    @name_or_ticker
    def __init__(self, ticker: str = None, **kwargs):
        self.ticker = ticker

        if not is_company_available_domestic(ticker=self.ticker):
            if is_company_available_online(ticker=self.ticker):
                add_company_domestic(self.ticker)
                self.is_available = True

            else:
                self.is_available = False

        else:
            self.is_available = True

        if self.is_available:
            self.info = get_company_dict(ticker=self.ticker)

        else:
            self.info = None

    def get_ticker(self) -> str:
        return self.ticker

    def get_info(self) -> dict | None:
        return self.info

    def get_name(self) -> str | None:
        if not self.is_available:
            return
        return self.info['name']

    def get_stocks(self, start: datetime.datetime, end: datetime.datetime, interval: str) -> pandas.DataFrame:
        return get_stocks(ticker=self.ticker, start=start, end=end, interval=interval)

    def get_stocks_any_format(self, start: datetime.datetime, end: datetime.datetime, interval: str, data_format: str):
        if not self.is_available or data_format not in self.all_formats:
            return

        df = self.get_stocks(start, end, interval)
        if data_format == 'close_prices_list':
            return [row[4] for row in df.itertuples(name='Candle')]

        elif data_format == 'list_for_graph_line':
            return [[row[0].__str__(), (row[1] + row[4]) / 2] for row in df.itertuples()]

        elif data_format == 'list_for_graph':
            return [[row[0].__str__(), row[3], row[1], row[4], row[2]] for row in df.itertuples()]

        elif data_format == 'stocks_list':
            return [row for row in df.itertuples(name='Candle')]

