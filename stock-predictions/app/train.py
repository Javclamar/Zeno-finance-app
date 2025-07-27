from app.data import preprocessing, create_sequences, download_historical_data, download_recent_data, get_historical_data_alpaca, get_recent_data_alpaca
from app.model import build_model
import pickle
import os

# Training ad saving of the LSTM model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEW_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "new_stock_data.csv")
HISTORICAL_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "historical_stock_data.csv")

def train():

    get_historical_data_alpaca()
    get_recent_data_alpaca()

    df_scaled, scalers, le = preprocessing(HISTORICAL_DATA_PATH) # Returns the df, the scalers used for the unique tickers, and the label encoder used for the ticjer encoding
    X_seq, y, ticker_ids, X_dow = create_sequences(df_scaled) # Creates 60 days sequence used to predict the next days close, returning the X, y df
    num_tickers = len(le.classes_)

    # Train test splitting (needs to be done like this to dont shuffle the time series)
    split = int(0.8 * len(X_seq))
    X_train, X_test = X_seq[:split], X_seq[split:]
    y_train, y_test = y[:split], y[split:]
    ticker_train, ticker_test = ticker_ids[:split], ticker_ids[split:]
    X_dow_train, X_dow_test = X_dow[:split], X_dow[split:]



    model = build_model(60, num_tickers=num_tickers, num_features=6)

    print(f"X shape: {X_seq.shape}")
    print(f"y shape: {y.shape}")

    # Save the scaler and encoder to use for the predictions inverse scaling and encoding
    with open('models/scalers.pkl', 'wb') as f:
        pickle.dump(scalers, f)

    with open('models/label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)

    model.fit(
        [X_train, ticker_train, X_dow_train], y_train,
        validation_data=([X_test, ticker_test, X_dow_test], y_test),
        epochs=20,
        batch_size=32
    )

    model.save('./models/stock_lstm_model.keras')

if __name__ == "__main__":
    train()
