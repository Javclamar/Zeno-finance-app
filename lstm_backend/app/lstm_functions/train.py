from app.lstm_functions.data import preprocessing, create_sequences, get_historical_data_alpaca, get_recent_data_alpaca
from app.lstm_functions.model import build_model
import pickle
import os
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# Training ad saving of the LSTM model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEW_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "new_stock_data.csv")
HISTORICAL_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "historical_stock_data.csv")
LSTM_UTILS = os.path.join(BASE_DIR, '..', 'lstm_utils')


def train():

    get_historical_data_alpaca()
    get_recent_data_alpaca()

    df_scaled, scalers, le = preprocessing(HISTORICAL_DATA_PATH) # Returns the df, the scalers used for the unique tickers, and the label encoder used for the ticker encoding
    X_seq, y, ticker_ids, X_dow = create_sequences(df_scaled) # Creates 60 days sequence used to predict the next days close, returning the X, y df
    num_tickers = len(le.classes_)

    # Train test splitting (needs to be done like this to dont shuffle the time series)
    split = int(0.8 * len(X_seq))
    X_train, X_test = X_seq[:split], X_seq[split:]
    y_train, y_test = y[:split], y[split:]
    ticker_train, ticker_test = ticker_ids[:split], ticker_ids[split:]
    X_dow_train, X_dow_test = X_dow[:split], X_dow[split:]



    model = build_model(60, num_tickers=num_tickers, num_features=8)

    print(f"X shape: {X_seq.shape}")
    print(f"y shape: {y.shape}")

    # Save the scaler and encoder to use for the predictions inverse scaling and encoding
    with open(os.path.join(LSTM_UTILS, 'scalers.pkl'), 'wb') as f:
        pickle.dump(scalers, f)

    with open(os.path.join(LSTM_UTILS, 'label_encoder.pkl'), 'wb') as f:
        pickle.dump(le, f)
        
    model.fit(
        [X_train, ticker_train, X_dow_train], y_train,
        validation_data=([X_test, ticker_test, X_dow_test], y_test),
        epochs=20,
        batch_size=32
    )
    
    # Predict on test set
    y_pred_scaled = model.predict([X_test, ticker_test, X_dow_test])
    
    y_pred_real = []
    y_test_real = []


    for i in range(len(y_pred_scaled)):
        ticker_id = ticker_test[i][0]
        ticker = le.inverse_transform([ticker_id])[0]
        scaler = scalers[ticker]

        dummy_pred = np.zeros((1, 9))
        dummy_pred[0, -1] = y_pred_scaled[i].item()
        pred_real = scaler.inverse_transform(dummy_pred)[0, -1]
        y_pred_real.append(pred_real)

        dummy_true = np.zeros((1, 9))
        dummy_true[0, -1] = y_test[i].item()
        true_real = scaler.inverse_transform(dummy_true)[0, -1]
        y_test_real.append(true_real)

    # Calculate metrics
    r2_real = r2_score(y_test_real, y_pred_real)
    r2 = r2_score(y_test, y_pred_scaled)
    mae = mean_absolute_error(y_test_real, y_pred_real)
    rmse = np.sqrt(mean_squared_error(y_test_real, y_pred_real))
    print(f"R2 score on test set: {r2:.4f}")
    print(f"R2 score on real prices: {r2_real:.4f}")
    print(f"MAE score on test set: {mae:.4f}")
    print(f"RMSE score on test set: {rmse:.4f}")
    
    plt.figure(figsize=(12,6))

    # Plot real values
    plt.plot(y_test_real, label='Real Prices', color='black', linewidth=1)

    # Plot predicted values
    plt.plot(y_pred_real, label='Predicted Prices', color='red', alpha=0.7)

    plt.title('Predicted vs Real Prices')
    plt.xlabel('Sample index')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
        

    model.save(os.path.join(LSTM_UTILS, 'stock_lstm_model.keras'), 'wb')

if __name__ == "__main__":
    train()
