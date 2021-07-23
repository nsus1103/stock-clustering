import config
import psycopg2
import psycopg2.extras

def createTable(cols):
    # Connect to Postgres SQL server. Credentials imported from config.py
    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER,
                                  password=config.DB_PASS)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # cursor.execute("""SELECT * FROM toy""")
    # print(cursor.fetchall())
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS stock_fundamentals(
                            
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(50))
                        """)
    except:
        print("Unable to create table")

    connection.commit()



createTable()