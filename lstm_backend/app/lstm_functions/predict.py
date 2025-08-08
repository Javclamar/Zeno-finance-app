import os
from keras.models import load_model
import pickle
import pandas as pd
import numpy as np
import json
from app.lstm_functions.data import load_stock_data
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session 
import asyncio
import pandas_ta as ta


# Function used to predict the next day close for the tickers in the dataset
async def predict_new_data(db: AsyncSession):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "..", "lstm_utils", "stock_lstm_model.keras")
    SCALER_PATH = os.path.join(BASE_DIR, "..", "lstm_utils", "scalers.pkl")
    ENCODER_PATH = os.path.join(BASE_DIR, "..", "lstm_utils", "label_encoder.pkl")
    PREDICTIONS_PATH = os.path.join(BASE_DIR, "..", "data", "latest_predictions.json")

    # Load the model, scalers and encoders used in training to ensure cohesion
    N = 60
    columns = ['Open', 'Close', 'High', 'Low', 'Volume', 'Target', 'RSI', 'SMA_20']

    if os.path.exists(PREDICTIONS_PATH):
        with open(PREDICTIONS_PATH, 'r') as f:
            predictions = json.load(f)
        return predictions
    
    model = load_model(MODEL_PATH)
    print(model.summary())
    predictions = {}

    with open(SCALER_PATH, 'rb') as f:
        scalers = pickle.load(f)
    with open(ENCODER_PATH, 'rb') as f:
        le = pickle.load(f)

    # Read the pre-downloaded csv and adds a dummy column
    df = await load_stock_data(db, 100)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Ticker', 'Date'])
    df['Target'] = df.groupby('Ticker')['Close'].shift(-1)
    df['Day_of_the_week'] = df['Date'].dt.dayofweek
    df.dropna(inplace=True)

    for ticker in df['Ticker'].unique():
        # Get all data for this ticker and sort by date
        df_ticker = df[df['Ticker'] == ticker].copy().sort_values('Date')
        
        # Calculate technical indicators on the full dataset
        df_ticker['RSI'] = ta.rsi(df_ticker['Close'], length=14)
        df_ticker['SMA_20'] = ta.sma(df_ticker['Close'], length=20)
        df_ticker.dropna(inplace=True)

        if len(df_ticker) < N:
            print(f"⚠️ Not enough data for {ticker}")
            continue

        # Get last N rows for sequence
        df_sequence = df_ticker.iloc[-N:]
        print(df_sequence.tail())
        
        # Create DataFrame with columns in exact same order as training
        scaling_df = pd.DataFrame()
        for col in columns:
            if col == 'Target':
                scaling_df[col] = np.nan
            else:
                scaling_df[col] = df_sequence[col]
        
        # Scale the features using all columns (including Target)
        scaler = scalers[ticker]
        scaled_values = scaler.transform(scaling_df)
        
        # Remove the Target column for the LSTM input (it's in position 5)
        feature_columns = [col for col in columns if col != 'Target']
        scaled_features = np.delete(scaled_values, 5, axis=1)  # Remove Target column
        
        # Create sequence for LSTM
        seq = np.expand_dims(scaled_features, axis=0)  # Shape will be (1, 60, 7)

        # We encode using the same LabelEncoder from training
        ticker_id = le.transform([ticker])[0]
        ticker_input = np.array([[ticker_id]])

        # We get the day of the week of the last day in the sequence
        dow = df_ticker['Day_of_the_week'].values[-1]
        dow_input = np.array([[dow]])
        
        # We do our prediction and do the inverse scaling
        pred_scaled = model.predict([seq, ticker_input, dow_input])[0][0] # This returns array([[prediction]]), since there is only one sample (<<1>>, length, num_features) we do [0][0] to only get the number                              
        
        # The scaler expects the same number of columns on the Array, right now we only have one (prediction)
        # Add as many dummy columns as many features used filled with 0
        # We put the prediction in the last column to match the Target column
        dummy = np.zeros((1, len(feature_columns) + 1))  # +1 for Target
        dummy[0, -1] = pred_scaled  # Put predicted value in Target position
        
        # Inverse transform to get real price
        pred_real = scaler.inverse_transform(dummy)[0, -1]
        predictions[ticker] = pred_real
        
    if predictions == {}:
        print("⚠️ No predictions made, check the data or model.")
    else:
        with open(PREDICTIONS_PATH, 'w') as f:
            json.dump(predictions, f)
    
    print("✅ Predictions:")
    for ticker, price in predictions.items():
        print(f"{ticker}: {price:.2f}")

    return predictions

async def main():
    async with async_session() as db:
        await predict_new_data(db)

if __name__ == "__main__":
    asyncio.run(main())