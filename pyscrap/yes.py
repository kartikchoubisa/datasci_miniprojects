from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import numpy as np
import itertools as it

url = "https://finance.yahoo.com/quote/MSFT/balance-sheet/"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
table = soup.find("div", attrs={"data-reactid":"51"}).children
# print(len(list(table))) # 2
columns = next(table)
columns = pd.Series((content.get_text() for content in columns.find_all("span")))

data = next(table)

data = [e.get_text() for e in data.find_all("span")]

def reshape_data(d: list) -> list:
    new = []

    for e in d:
        if e[0].isalpha():
            new.append([])
        new[-1].append(e)
    return new

data = reshape_data(data)
df = pd.DataFrame(data, columns= columns)


print(df)