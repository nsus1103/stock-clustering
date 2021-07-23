import pandas as pd
import psycopg2
import psycopg2.extras
import config
import numpy as np


"""
cursor.execute("SELECT * FROM toy")
print("Testing DB connection.",cursor.fetchall())
"""

def get_price_change(ticker):
    df = pd.read_csv(f'./S&P500/{ticker}.csv', parse_dates=['date'])
    df['percent_change'] = (df.close - df.close.shift())*100/df.close
    return df

def write_daily_price_to_db(ticker, df):

    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER,
                                  password=config.DB_PASS)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("""SELECT DISTINCT stock_id FROM daily_price""")
    stock_in_db = cursor.fetchall()

    for _, day in df.iterrows():

        try:
            cursor.execute("""SELECT id FROM stock WHERE symbol = %(ticker)s""", {"ticker":ticker})
            ticker_id = cursor.fetchone()[0]
            if ticker_id not in stock_in_db:
                cursor.execute("""
                INSERT INTO daily_price(stock_id, dt, open, high, low, close, volume)
                VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                               (ticker_id, day.date, day.open, day.high, day.low, day.close, day.volume))
        except Exception as e:
            print("Ticker not found. Error:", e)
            connection.rollback()
            break
        connection.commit()

def get_price_change_from_db(ticker_id):
    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER,
                                  password=config.DB_PASS)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cursor.execute(f"""SELECT d1.dt, (d1.close-d2.close)*100/d2.close AS percent_change
                        FROM daily_price AS d1
                        INNER JOIN daily_price AS d2
                        ON d1.dt = d2.dt + INTERVAL '1 day' AND d1.stock_id = d2.stock_id
                        WHERE d1.stock_id = {ticker_id} AND EXTRACT(YEAR FROM d1.dt)>2010 AND EXTRACT(YEAR FROM d1.dt)<2021
                        ORDER BY d1.dt DESC """)
        data = cursor.fetchall()
        d, p = zip(*data)
        dates = [d1.strftime("%d-%b-%Y") for d1 in d]
        per_change = [float(p1) for p1 in p]
    except Exception as e:
        print(e)
        connection.rollback()
        price = None
    connection.commit()

    return dates, per_change

def get_ticker_within_date_range(year_start, year_end):
    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER,
                                  password=config.DB_PASS)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute(f""" SELECT stock_id
                        FROM daily_price
                        GROUP BY stock_id
                        HAVING EXTRACT(YEAR FROM MIN(dt))<{year_start} AND EXTRACT(YEAR FROM MAX(dt))>{year_end}
                        ORDER BY MIN(dt) DESC;""")
        ticker_ids = cursor.fetchall()
    except Exception as e:
        print(e)
        connection.rollback()
        ticker_ids = None
    connection.commit()
    return ticker_ids

def write_sectors_to_db():

    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER,
                                  password=config.DB_PASS)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    sp = pd.read_csv('constituents.csv')
    sectors = sorted(sp['Sector'].unique())

    for index, sector in enumerate(sectors):
        try:
            cursor.execute("""INSERT INTO sp_sectors (sector_id, sector_name) VALUES(%s, %s)""", (index+1, sector))
        except Exception as e:
            print(e)
            connection.rollback()
        connection.commit()
    return

def get_stock_symbols(tickers):

    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER,
                                  password=config.DB_PASS)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    symbol_dict = {}
    symbols=[]
    for ticker in tickers:
        try:
            cursor.execute(f"""SELECT symbol FROM stock WHERE id = {ticker[0]}""")
            f = cursor.fetchone()
            symbol_dict[ticker[0]] = f[0]
            symbols.append(f[0])
        except Exception as e:
            print(e)
            connection.rollback()
            symbol_dict = None
        connection.commit()

    return symbols


# def main():

tickers = get_ticker_within_date_range(2010, 2020)
# tickers = [5]

price_df = pd.DataFrame()
s_id=[]

for ticker in tickers:
    dates, change = get_price_change_from_db(ticker[0])
    temp_df = pd.DataFrame([change], columns=dates)
    print(len(temp_df.columns), temp_df.columns[0], temp_df.columns[-1])
    price_df = price_df.append(temp_df)
    s_id.append(ticker[0])

price_df['symbol'] = get_stock_symbols(tickers)

# if __name__ == '__main__':
#     main()