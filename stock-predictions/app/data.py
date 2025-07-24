import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from datetime import datetime, timedelta

tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'BAC', 'SPY', 'QQQ'] # Tickers that we will predict

# Downloads the data used to train the model, this will be used in training
def download_historical_data():
    data = yf.download(tickers, start='2020-01-01', group_by='ticker')
    dfs = []
    for ticker in tickers:
        df = data[ticker].copy()
        df['Ticker'] = ticker
        df['Date'] = df.index
        dfs.append(df.reset_index(drop=True))
    df_all = pd.concat(dfs)
    df_all.sort_values(['Ticker', 'Date'], inplace=True)
    df_all.to_csv('./data/historical_stock_data.csv', index=False)
    print("✅ Data saved to historical_stock_data.csv")

# Downloads the data used to make predictions. This could be swapped with a query to a MongoDB in the feature so we dont have 2 different datasets
def download_recent_data():
    start = datetime.today().date() - timedelta(days=100)
    start_str =  start.strftime('%Y-%m-%d')

    data = yf.download(tickers, start=start_str, group_by='ticker')
    dfs = []
    for ticker in tickers:
        df = data[ticker].copy()
        df['Ticker'] = ticker
        df['Date'] = df.index
        dfs.append(df.reset_index(drop=True))
    df_all = pd.concat(dfs)
    df_all.sort_values(['Ticker', 'Date'], inplace=True)
    df_all.to_csv('./data/new_stock_data.csv', index=False)
    print("✅ Data saved to new_stock_data.csv")

# Preprocessing of the data, scaling, encoding and sorting by ticker and date to create the time-series for each ticker
def preprocessing(csv_path):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # Create the target value, that  is the Close value of the next day (row in this case)
    df['Target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)

    df_scaled = []
    scalers = {}
    columns = ['Open', 'Close', 'High', 'Low', 'Volume', 'Target']

    # Scale the data by ticker, since the values can differ a lot depending on the ticker we cant scale all at once
    for ticker in df['Ticker'].unique():
        scaler = MinMaxScaler()
        df_ticker = df[df['Ticker'] == ticker].copy()
        
        scaled_values = scaler.fit_transform(df_ticker[columns])
        
        df_ticker_scaled = pd.DataFrame(scaled_values, columns=columns, index=df_ticker['Date'])
        df_ticker_scaled['Ticker'] = df_ticker['Ticker'].values
        
        df_scaled.append(df_ticker_scaled)
        scalers[ticker] = scaler

    df_scaled = pd.concat(df_scaled)

    # Encode the Ticker column
    le = LabelEncoder()
    df_scaled['Ticker'] = le.fit_transform(df_scaled['Ticker'])
    print("Data after preprocessing:\n", df_scaled.head())
    return df_scaled, scalers, le

# Creates a N days sequence of data and returns the X df( Values ), y df( Target ) and tickers_labels
def create_sequences(df, N=60, columns=['Open', 'Close', 'High', 'Low', 'Volume'], target='Target'):
    X, y, ticker_ids = [], [], []

    for ticker in df['Ticker'].unique():
        df_ticker = df[df['Ticker'] == ticker].sort_values('Date')
        data = df_ticker[columns].values
        targets = df_ticker[target].values

        for i in range(len(data) - N):
            X.append(data[i:i+N])
            y.append(targets[i+N])
            ticker_ids.append(ticker)
    
    return np.array(X), np.array(y), np.array(ticker_ids)

