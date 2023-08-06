import requests
import json
import pandas as pd

BASE_URL = "https://stocksera.pythonanywhere.com/api/"


class ETF:
    def jim_cramer(self):
        r = requests.get(f"{BASE_URL}/jim_cramer")
        j = json.loads(r.content)
        return pd.DataFrame(j)
