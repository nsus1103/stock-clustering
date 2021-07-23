import functions
import pandas as pd
import os

files = os.listdir('./S&P500')
stock_populated = []

# list of all stocks in db
for f in files:
    stock_populated.append(f.strip('.csv'))
print(f"{len(stock_populated)} stocks populated")

for stock in stock_populated:
    stockdf = pd.read_csv(f'./S&P500/{stock}.csv')
    functions.write_to_db(stock, stockdf)