import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import requests

class fin_data_set():
    def __init__(self, body_dict: dict, meta_data_dict: dict):
        #this step removes the garbage from the keys
        meta_data_dict_clean = self.clean_dictionary(meta_data_dict)

        self.symbol = meta_data_dict_clean['Symbol']
        self.interval = meta_data_dict_clean['Interval']
        self.time_zone = meta_data_dict_clean['Time Zone']

        self.df = pd.DataFrame.from_dict(body_dict, orient="index").astype(float)
        self.df.columns = [re.sub(r'^\d+\.\s*', '', c) for c in self.df.columns]

    def clean_dictionary(self, d: dict) -> dict:
        return {re.sub(r'^\d+\.\s*', '', k): v for k, v in d.items()}

    def print(self) -> None:
        print(f" Symbol: {self.symbol}, Interval: {self.interval}, Time Zone: {self.time_zone}")
        print("rest of the data...")
        print(self.df)

    def simple_graph(self) -> None:
        self.df['close'].plot()
        plt.show()


class fin_data_access():
    def __init__(self):
        self.api_key = '5GIDPTJKKUVGRUC3'

    def get_data(self, symbol: str, interval: str) -> fin_data_set:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": self.api_key,
            "datatype": "json",
        }
        r = requests.get("https://www.alphavantage.co/query?", params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if "Error Message" in data or "Note" in data:
            raise ValueError(data.get("Error Message") or data.get("Note"))
        
        print(data)
    
        #convert to fin_data_set type
        meta_data = data['Meta Data']
        body_data_key = next((k for k in data.keys() if 'Time Series' in k ), None)
        body_data = data[body_data_key]

        return fin_data_set(body_data, meta_data)

def run():
    # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=5GIDPTJKKUVGRUC3'
    # r = requests.get(url)
    # data = r.json()
    # # print(data)

    # # print(data.keys())

    # meta_data = data['Meta Data']
    # body_data_key = next((k for k in data.keys() if 'Time Series' in k ), None)
    # body_data = data[body_data_key]

    # body_keys = len(body_data.keys())
    # print(body_keys)

    # print(meta_data)


    data_access = fin_data_access()
    data = data_access.get_data("IBM", "5m")

    data.print()
    data.simple_graph()




if __name__ == '__main__':
    run()
