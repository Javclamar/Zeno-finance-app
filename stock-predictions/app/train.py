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

    y_pred_scaled = model.predict([X_test, ticker_test]).flatten()
    y_pred_real, y_test_real = [], []

    for pred_scaled, real_scaled, ticker_id in zip(y_pred_scaled, y_test, ticker_test.flatten()):

        ticker_name = le.inverse_transform([ticker_id])[0]
        scaler = scalers[ticker_name]
        
        dummy = np.zeros((1, len(['Open', 'Close', 'High', 'Low', 'Volume', 'Target'])))
        dummy[0, -1] = pred_scaled
        pred_real = scaler.inverse_transform(dummy)[0, -1]
        y_pred_real.append(pred_real)

        dummy[0, -1] = real_scaled
        real = scaler.inverse_transform(dummy)[0, -1]
        y_test_real.append(real)
    
    y_pred_real = np.array(y_pred_real)
    y_test_real = np.array(y_test_real)

    plt.figure(figsize=(12,6))
    plt.plot(y_test_real[1:201], label='Real Close')
    plt.plot(np.roll(y_pred_real, -1)[:200], label='Predicted Close')
    plt.title("Predicted vs Real Close Prices (first 200 test samples)")
    plt.xlabel("Sample")
    plt.ylabel("Close price")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    train()
