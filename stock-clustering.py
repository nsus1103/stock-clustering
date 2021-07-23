import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('daily_price_change.csv')
sectors = pd.read_csv('constituents.csv')
val_df = sectors[sectors.Symbol.isin([l for l in df.symbol])]

labels = LabelEncoder().fit_transform(val_df.Sector)

cl = AgglomerativeClustering(n_clusters=11, linkage="average")
cl.fit(df.drop('symbol', axis=1))

print(confusion_matrix(labels, cl.labels_))