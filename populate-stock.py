
import config
import psycopg2
import psycopg2.extras
import alpaca_trade_api as tradeapi

#Connect to Postgres SQL server. Credentials imported from config.py
connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

#Aplaca API to populate stocks symbols
api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)

assets = api.list_assets()

for asset in assets:
    print(f"Inserting stock {asset.name} {asset.symbol}")
    cursor.execute("""
        INSERT INTO stock (name, symbol, exchange, isEtf)
        VALUES (%s, %s, %s, %s)
    """, (asset.name, asset.symbol, asset.exchange, False))

connection.commit()

try:
    cursor.execute("SELECT COUNT(*) FROM stock")
    rows = cursor.fetchall()
    print('Total Count of Stocks populated:',rows)
except Exception as e:
    print(e)
    connection.rollback()