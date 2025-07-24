from app.data import preprocessing, create_sequences
from app.model import build_model
import pickle
import matplotlib.pyplot as plt
import numpy as np

def train():
    
    df_scaled, scalers, le = preprocessing('./data/historical_stock_data.csv')
    X, y, ticker_ids = create_sequences(df_scaled)
    num_tickers = len(le.classes_)

    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    ticker_train, ticker_test = ticker_ids[:split], ticker_ids[split:]


    model = build_model(60, num_tickers=num_tickers, num_features=5)

    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")

    with open('models/scalers.pkl', 'wb') as f:
        pickle.dump(scalers, f)

    with open('models/label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)

    model.fit(
        [X_train, ticker_train], y_train,
        validation_data=([X_test, ticker_test], y_test),
        epochs=20,
        batch_size=32
    )

    model.save('./models/stock_lstm_model.keras')

if __name__ == "__main__":
    train()
