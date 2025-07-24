from keras.models import load_model
import pickle
import pandas as pd
import numpy as np

# Function used to predict the next day close for the tickers in the dataset
def predict_new_data():

    # Load the model, scalers and encoders used in training to ensure cohesion
    N = 60
    columns = ['Open', 'Close', 'High', 'Low', 'Volume']
    model = load_model('./models/stock_lstm_model.keras')
    predictions = {}

    with open('models/scalers.pkl', 'rb') as f:
        scalers = pickle.load(f)
    with open('models/label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)

    # Read the pre-downloaded csv and adds a dummy column
    df = pd.read_csv('./data/new_stock_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Target'] = 0


    for ticker in df['Ticker'].unique():
        df_ticker = df[df['Ticker'] == ticker].copy().sort_values('Date') # Sort by date the data of the ticker

        if len(df_ticker) < N:
            print(f"⚠️ Not enough data for {ticker}")
            continue

        # Scaling of the data using the same scaler as in training
        scaler = scalers[ticker]
        scaled_vals = scaler.transform(df_ticker[columns + ['Target']])
        scaled_df = pd.DataFrame(scaled_vals, columns=columns + ['Target'])

        # We take the last N rows (days)
        seq = scaled_df[columns].values[-N:]
        seq = np.expand_dims(seq, axis=0) # The model expects a shape of (samples, length, num_features): seq has already (length, num_features) so we expand to (1, length, num_features)

        # We encode using the same LabelEncoder from training
        ticker_id = le.transform([ticker])[0]
        ticker_input = np.array([[ticker_id]])

        # We do our prediction and do the inverse scaling
        pred_scaled = model.predict([seq, ticker_input])[0][0] # This returns array([[prediction]]), since there is only one sample (<<1>>, length, num_features) we do [0][0] to only get the number                              
        
        # The scaler expects the same number of columns on the Array, right now we only have one (prediction)
        # Add as many dummy columns as many features used filled with 0
        # We put the prediction in the last column to match the Target column
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