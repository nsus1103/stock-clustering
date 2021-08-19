# stock-clustering

Python project to determine stocks that exhibit similar price action.

## Description
Data: Data is collected from SIMFIN API (free version) using Asynchronous request for concurrency and <br>
faster HTML response. The data is OHLCV data for the stocks in the PostgreSQL populated earlier. The data <br>
is stored as a csv and later populated into a SQL table. The database contains other tables like stock symbol, <br>
ETF composition etc.<br>
The data is ingested into pandas dataframe using Dynamic SQL (psycopg2) and unsupervised clustering algorithm <br>is implemented.

## 1. Setting up Postgres Instance
To create the postgres instance on docker

>docker pull postgres

To start a postgres instance

> docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres

The postgres instance name and password will be used to connect to the database using psycopg2

## 2. Setting up API

Create account with SIMFIN and Alphavantage for the api key.
https://simfin.com/data/api <br>
https://www.alphavantage.co/

## 3. Setup config

Enter the postgres database credentials and the API key in the config.py template file in the repository


## 4. Setting the Postgres database

Create a database and required tables by running the script etfdb.sql or by copy pasting the scripts in the terminal.


## 5. Populating the tables

Run the script populate-stocks.py and populate-timeseries.py to pull all stocks and price data for alst ten years using API. This will take a few hours to complete depending on whether account associated with API is free or premium

## 6. Stock cluster analysis

The script for training the unsupervised clustering model is in train.py. 
The script app.py is the front end design and can be run by following command. The webpage can be visited on local

> streamlit run app.py

The console will display the address where the web app is being hosted. It will be localhost followed by a port (eg: http://localhost:8502/)

This is the homepage
![image](https://user-images.githubusercontent.com/33731048/130132365-95e1ae1c-9c08-4ad5-b4d8-c4a5b1e13994.png)

Here we can select the dates between which to carry out the cluster analysis and choose the model

Once the data is pulled from database, it will show the first 5 rows.

![image](https://user-images.githubusercontent.com/33731048/130132608-a12f12fc-5b92-4a23-aa18-bb8c99681e53.png)

Click on start training to run the model. Once completed, we can view the clusters in an interactive 3d plot.

![image](https://user-images.githubusercontent.com/33731048/130132966-00559e16-fbb3-4efe-b3e0-16c50c569d5e.png)
![image](https://user-images.githubusercontent.com/33731048/130133069-9fd867c7-f6de-44d2-9487-d6eabb11ab19.png)






