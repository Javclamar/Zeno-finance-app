from keras.models import load_model
import pickle
from app.data import preprocessing, create_sequences
import pandas as pd
import numpy as np

def predict_new_data():
    N = 60
    columns = ['Open', 'Close', 'High', 'Low', 'Volume']
    model = load_model('./models/stock_lstm_model.keras')
    predictions = {}

    with open('models/scalers.pkl', 'rb') as f:
        scalers = pickle.load(f)
    with open('models/label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)

    df = pd.read_csv('./data/new_stock_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Target'] = 0

    for ticker in df['Ticker'].unique():
        df_ticker = df[df['Ticker'] == ticker].copy().sort_values('Date')

        if len(df_ticker) < N:
            print(f"⚠️ Not enough data for {ticker}")
            continue
        scaler = scalers[ticker]
        scaled_vals = scaler.transform(df_ticker[columns + ['Target']])
        scaled_df = pd.DataFrame(scaled_vals, columns=columns + ['Target'])

        seq = scaled_df[columns].values[-N:]
        seq = np.expand_dims(seq, axis=0)

        ticker_id = le.transform([ticker])[0]
        ticker_input = np.array([[ticker_id]])

        pred_scaled = model.predict([seq, ticker_input])[0][0]
        dummy = np.zeros((1, len(columns) + 1))
        dummy[0, -1] = pred_scaled

        pred_real = scaler.inverse_transform(dummy)[0, -1]

        predictions[ticker] = pred_real
    
    print("✅ Predictions:")
    for ticker, price in predictions.items():
        print(f"{ticker}: {price:.2f}")

    return predictions

if __name__ == "__main__":
    predict_new_data()