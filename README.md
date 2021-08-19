# stock-clustering

Python project to determine stocks that exhibit similar price action.

## Description
Data: Data is collected from SIMFIN API (free version) using Asynchronous request for concurrency and <br>
faster HTML response. The data is OHLCV data for the stocks in the PostgreSQL populated earlier. The data <br>
is stored as a csv and later populated into a SQL table. The database contains other tables like stock symbol, <br>
ETF composition etc.<br>
The data is ingested into pandas dataframe using Dynamic SQL (psycopg2) and unsupervised clustering algorithm <br>is implemented.

## 1. Setting up Database
To create the postgres instance on docker

>docker pull postgres

To start a postgres instance

> docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres

The postgres instance name and password will be used to connect to the database using psycopg2

## 2. Setting up API

Create free account with SIMFIN for the api key.
https://simfin.com/data/api

## 3. Setup config

Enter the postgres database credentials and the API key in the config.py template file in the repository







