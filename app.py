"""
To run use following command in terminal
$ streamlit run app.py
"""

import utils
import pandas as pd
import streamlit as st
import datetime
import train

st.title("Cluster Analysis on Stock price")


date_start = pd.to_datetime(st.sidebar.date_input('Start date (after 01/01/2011)', datetime.date(2020, 12, 1)))
date_end = pd.to_datetime(st.sidebar.date_input('End date (before 01/06/2021)', datetime.date(2020, 12, 31)))

# Add a selectbox to the sidebar:
model_select = st.sidebar.selectbox(
    'Clustering method',
    (" ","KMeans", "Agglomerative")
)

st.write("Start date for analysis:", date_start.date())
st.write("End date for analysis:", date_end.date())
st.write("Model for analysis:", model_select)

load_data=False

# Read data from database
price_change_data = utils.get_percent_change_within_date_range(date_start=date_start, date_end=date_end)

if st.button('Load data'):

    st.write("Data ready! Here are the first 5 rows")
    load_data=True

    first5 = train.print_head(price_change_data)
    st.write(first5)


# KMeans Clustering
start_training = st.button('Start Training')
if start_training:
    st.write("Training")
    fig, results = train.train_classifier(price_change_data)

    st.write("Training complete")

    # view results summary
    view_results = st.checkbox("View results")
    if view_results:
        st.write(results)

    st.plotly_chart(fig)



