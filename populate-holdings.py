import requests
import psycopg2
import psycopg2.extras
import datetime
import config

def populate_holdings(etfId, date, tickerId, ticker):

    print(f"Inserting tickerID {tickerId} {ticker['company']}")
    try:
        cursor.execute("""
        INSERT INTO holding(etfId, date, stockId, numShares, marketValue, weight)
        VALUES(%s, %s, %s, %s, %s, %s)""", (etfId, date,tickerId, ticker['shares'],
                                            ticker['market_value'], ticker['weight']))

    except Exception as e:
        print(e)
        connection.rollback()

    connection.commit()
    return


#Connect to Postgres SQL server. Credentials imported from config.py
connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

cursor.execute("SELECT * FROM toy")

print(cursor.fetchall())

ark_symbols = ['ARKK', 'ARKQ', 'ARKW', 'ARKG', 'ARKF', 'PRNT', 'IZRL']
ark_symbols_single = ['ARKK']
# base_url = 'https://arkfunds.io/api/v1/'
# etf_profile = 'etf/profile?symbol='
# etf_holding = 'etf/holdings?symbol='
# etf_trades = 'etf/trades?symbol='
# stock_profile = 'stok/profile?symbol='

holding_url = 'https://arkfunds.io/api/v1/etf/holdings'


newTickers = {}
for symbol in ark_symbols:
    params = {'symbol':symbol}
    response = requests.get(holding_url, params = params)
    etf = response.json()['symbol']
    date = datetime.datetime.strptime((response.json()['date']), '%Y-%m-%d').date()
    portfolio = response.json()['holdings']

    try:
        cursor.execute(f"SELECT id FROM stock WHERE symbol='{symbol}'")
        etfid = cursor.fetchall()
    except Exception as e:
        print(e)
        connection.rollback()


    weight = 0
    if response.status_code==200:
        for ticker in portfolio:
            weight = weight+ticker['weight']
            try:
                cursor.execute(f"SELECT id FROM stock WHERE symbol='{ticker['ticker']}'")
                tickerId = cursor.fetchall()
                if len(tickerId)==0:
                    newTickers[ticker['company']]=ticker['ticker']

            except Exception as e:
                print(e)
                connection.rollback()
            if len(tickerId)>0:
                print(f"sending{ticker['ticker']}, {tickerId}")
                populate_holdings(etfid[0][0], date, tickerId[0][0], ticker)



