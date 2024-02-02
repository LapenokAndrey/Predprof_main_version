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

    app.run()