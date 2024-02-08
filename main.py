import time
from backendAndData.flask_function import app
from backendAndData.online_functions import *
from strategy.strategy import *
from backendAndData.data_functions import *


if __name__ == '__main__':
    # set_empty_companies_json_domestic()
    app.run()

    start_time0 = datetime.datetime(2015, 1, 1)
    end_time0 = datetime.datetime.now()

    start_time1 = datetime.datetime(2008, 1, 1)
    end_time1 = datetime.datetime(2019, 1, 1)

    start_time2 = datetime.datetime(2012, 1, 1)
    end_time2 = datetime.datetime(2020, 1, 1)
