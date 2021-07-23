import asyncio
import aiohttp
import asyncpg
import pandas as pd
import psycopg2
import psycopg2.extras
import config
import requests
import re

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        print("FETCH:",url)
        r = await session.get(url)
        stock_response = await r.json()
        return stock_response


async def write_to_df(stock_json, stock_df):
    d = pd.DataFrame(stock_json[0]['data'], columns=stock_json[0]['columns'])
    print(d)
    # stock_df = stock_df.append(d)
    return


async def write_to_db(stock_json):
    print(stock_json)

    pass

async def main(stock_list, stock_df):

    tasks=[]
    for stock in stock_list:

        # ticker = stock[1]
        ticker = stock
        fundamental_parameters = {"api-key": config.SIMFIN_API_KEY, "ticker": ticker, "statement": "bs",
                                  "period": period, "fyear": fyear}
        furl = f"https://simfin.com/api/v2/companies/statements?api-key={config.SIMFIN_API_KEY}&ticker={ticker}&statement={statement}&period={period}&fyear={fyear}"


        if ticker not in stock_populated.keys():
            print(f'{ticker} not in database, requesting now...')
            ticker_response = await fetch(furl)
            print(ticker_response)
            if ticker_response[0]['found']:
                main.ticker_response = ticker_response
                # tasks.append(write_to_db(ticker_response))
                d = pd.DataFrame(ticker_response[0]['data'], columns=stock_json[0]['columns'])
                print(d)
                stock_df = stock_df.append(d)
                tasks.append(write_to_df(ticker_response, stock_df))


    await asyncio.gather(*tasks)
    return


parameters = {"api-key": config.SIMFIN_API_KEY}
companies_listurl = "https://simfin.com/api/v2/companies/list"
response = requests.get(companies_listurl, parameters)
r = response.json()
# stock_list = [data[1] for data in r['data']]
stock_list = ['AAPL', 'MSFT']

fundamental_url = "https://simfin.com/api/v2/companies/statements"
statements = ['pl', 'bs', 'cf', 'derived']
statement = 'bs'
periods = ["q1", "q2", "q3", "q4", "fy", "h1", "h2", "9m"]
period = "q1"
fyear = "2021"

fundamental_parameters = {"api-key": config.SIMFIN_API_KEY, "ticker": 'AAPL', "statement": "bs",
                          "period": period, "fyear": fyear}
furl = f"https://simfin.com/api/v2/companies/statements?api-key={config.SIMFIN_API_KEY}&ticker='AAPL',&statement={statement}&period={period}&fyear={fyear}"

col_response = requests.get(furl, fundamental_parameters).json()
dfcols = col_response[0]['columns']
cols2table = [re.sub('[^a-zA-Z0-9]+', '',_) for _ in dfcols]
stock_df = pd.DataFrame(columns=dfcols)
stock_populated = {}

asyncio.run(main(stock_list, stock_df))