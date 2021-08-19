import pandas as pd
import requests
import os

api_key = 'your_alphavantage_api_key_here'
sp500 = pd.read_csv('data/constituents.csv')
stock_list = sp500.Symbol

cols = ['1. open', '2. high', '3. low', '4. close', '5. adjusted close', '6. volume', '7. dividend amount', '8. split coefficient']
files = os.listdir('./daily-prices')
stock_populated = []

for f in files:
    stock_populated.append(f.strip('.csv'))
print(f"{len(stock_populated)} stocks populated")

for ticker in stock_list:
    df = pd.DataFrame()

    if ticker in stock_populated:
        print("skipping:", ticker)
        continue
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={api_key}'
    r = requests.get(url)
    response = r.json()
    #
    # def create_dataframe(cols):
    #     if df.shape[0] != 0:
    #         df = pd.DataFrame(columns=cols)
    #     return df
    try:
        for day in response['Time Series (Daily)'].keys():
            daily = response['Time Series (Daily)'][day]
            temp_df = pd.DataFrame(daily, index=[day])
            # df = create_dataframe(daily.keys())
            df = df.append(temp_df)
        df.to_csv(f'{ticker}.csv')
        stock_populated.append(ticker)
    except Exception as e:
        print(e, ticker, response)