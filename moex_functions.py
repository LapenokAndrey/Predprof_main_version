import pandas as pd
import requests

j = requests.get('http://iss.moex.com/iss/engines/stock/markets/shares/securities/YNDX/candles.json?from=2023-05-25&till=2023-09-01&interval=24').json()
data = [{k : r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
frame = pd.DataFrame(data)
print(frame.info())


def get_data_of_company_moex():
    ...
