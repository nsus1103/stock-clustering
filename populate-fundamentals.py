import requests
import config
import pandas as pd
import sys
import itertools
import csv

parameters = {"api-key": config.SIMFIN_API_KEY}
url = "https://simfin.com/api/v2/companies/list"
fundamental_url = "https://simfin.com/api/v2/companies/statements"
r = requests.get(url, parameters)
response = r.json()

statements = ['pl', 'bs', 'cf', 'derived']
periods = ["q1", "q2", "q3", "q4", "fy", "h1", "h2", "9m"]
period = "q1"
fyear = "2021"

stock_populated = {}

for data in response['data']:
    ticker = data[1]
    fundamental_parameters = {"api-key": config.SIMFIN_API_KEY, "ticker": ticker, "statement": "bs",
                              "period": period, "fyear": fyear}
    if ticker not in stock_populated.keys():
        print(f'{ticker} not in database, requesting now...')
        stock_response = requests.get(fundamental_url, fundamental_parameters)
        s = stock_response.json()
        if s[0]['found']:
            stock_populated[ticker] = dict(zip(s[0]['columns'], s[0]['data'][0]))

# fields = s[0]['columns']
# w = csv.DictWriter( sys.stdout, fields )
# for key,value in stock_populated.items():
#     for key2, value2 in value:
#
#     row = {'org': key}
#     row.update(val)
#     w.writerow(row)