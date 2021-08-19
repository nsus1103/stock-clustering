import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.decomposition import PCA
import plotly.express as px

def print_head(df):
    df.dropna(axis=0, inplace=True)

    # Reading the actual labels from csv
    sectors = pd.read_csv('constituents.csv')

    df = pd.merge(df, sectors, left_on='symbol', right_on='Symbol').drop(['Symbol', 'Name'], axis=1)
    df = df.head()
    return df

def train_classifier(df):
    df.dropna(axis=0, inplace=True)

    # Reading the actual labels from csv
    sectors = pd.read_csv('constituents.csv')

    df = pd.merge(df, sectors, left_on='symbol', right_on='Symbol')
    # # val_df = sectors[sectors.Symbol.isin([l for l in df.symbol])]
    #
    df['Sector_label'] = LabelEncoder().fit_transform(df.Sector)
    cols2drop = ['symbol', 'name', 'Symbol', 'Name', 'Sector', 'Sector_label']

    # MinMax scaling
    scaler = MinMaxScaler()
    train_df = pd.DataFrame(scaler.fit_transform(df.drop(cols2drop, axis=1)),
                            columns=df.drop(cols2drop, axis=1).columns)

    kmeans_cl = KMeans(n_clusters=len(df.Sector_label.unique()))
    kmeans_cl.fit(train_df)
    results = classification_report(df.Sector_label, kmeans_cl.labels_)

    fig = plot_clusters(df, train_df, kmeans_cl)
    return fig, results

def plot_clusters(df, train_df, kmeans_cl):
    pca = PCA(n_components=3)
    plot_df = pd.DataFrame(pca.fit_transform(train_df), columns=['pc1', 'pc2', 'pc3'])

    fig = px.scatter_3d(plot_df, x='pc1', y='pc2', z='pc3',
                        color=kmeans_cl.labels_, size_max=10,
                        opacity=0.7, text=df['symbol'])

    # tight layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig

