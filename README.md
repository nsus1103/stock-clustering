# stock-clustering

Python project to determine stocks that exhibit similar price action.

## Description
Data: Data is collected from SIMFIN API (free version) using Asynchronous request for concurrency and faster HTML response. The data is OHLCV data for the stocks in the PostgreSQL populated earlier. The data is stored as a csv and later populated into a SQL table. The database contains other tables like stock symbol, ETF composition etc.
The data is ingested into pandas dataframe using Dynamic SQL (psycopg2) and unsupervised clustering algorithm is implemented.
