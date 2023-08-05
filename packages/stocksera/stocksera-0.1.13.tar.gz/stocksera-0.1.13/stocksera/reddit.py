import requests
import json
import pandas as pd

BASE_URL = "https://stocksera.pythonanywhere.com/api/"


class Reddit:
    def subreddit(self, ticker="GME"):
        r = requests.get(f"{BASE_URL}/subreddit_count/{ticker}")
        j = json.loads(r.content)
        return pd.DataFrame(j)

    def wsb_mentions(self, ticker=""):
        if not ticker:
            r = requests.get(f"{BASE_URL}/wsb_mentions")
        else:
            r = requests.get(f"{BASE_URL}/wsb_mentions/{ticker}")
        j = json.loads(r.content)
        return pd.DataFrame(j)

    def wsb_options(self, ticker=""):
        if not ticker:
            r = requests.get(f"{BASE_URL}/wsb_options")
        else:
            r = requests.get(f"{BASE_URL}/wsb_options/{ticker}")
        j = json.loads(r.content)
        return pd.DataFrame(j)