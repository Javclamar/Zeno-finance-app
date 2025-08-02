import os
from keras.models import load_model
from app.data import preprocessing, create_sequences

def test_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "stock_lstm_model.keras")
    HISTORICAL_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "historical_stock_data.csv")
    
    if not os.path.exists(MODEL_PATH):
        print("Model file does not exist.")
        return
    
    model = load_model(MODEL_PATH)
    print("Model loaded successfully.")
    
    
    
    
    model.summary()
    
    