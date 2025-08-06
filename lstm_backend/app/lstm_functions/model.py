from keras.layers import Embedding, Input, LSTM, Dense, Dropout, Concatenate, RepeatVector, Flatten
from keras.models import Model
from keras.losses import Huber
from keras import regularizers
from keras import optimizers
from keras.metrics import RootMeanSquaredError

# Input:
# N -> Number of days to predict the next days close
# num_tickers -> Number of tickers to predict
# num_features -> Number of features columns in the dataset
# emb_dim -> Dimension of the embedding layer
# This creates the LSTM model with 10 layers
def build_model(N, num_tickers, num_features, ticker_emb_dim=8, dow_emb_dim=3):

    seq_input = Input(shape=(N, num_features), name='seq_input')

    ticker_input = Input(shape=(1,), name='ticker_input')
    ticker_emb = Embedding(input_dim=num_tickers, output_dim=ticker_emb_dim, name='ticker_emb')(ticker_input)
    ticker_emb = Flatten()(ticker_emb)
    ticker_repeated = RepeatVector(N)(ticker_emb)

    dow_input = Input(shape=(1,), name='dow_input')
    dow_emb = Embedding(input_dim=7, output_dim=dow_emb_dim, name='dow_emb')(dow_input)
    dow_emb = Flatten()(dow_emb)
    dow_emb = Dropout(0.2)(dow_emb)
    dow_repeated = RepeatVector(N)(dow_emb)

    merged = Concatenate()([seq_input, ticker_repeated, dow_repeated])

    x = LSTM(64, return_sequences=True, recurrent_dropout=0.2, kernel_regularizer=regularizers.l2(0.001))(merged)
    x = Dropout(0.4)(x)
    x = LSTM(32)(x)
    x = Dropout(0.3)(x)
    output = Dense(1)(x)

    model = Model(inputs=[seq_input, ticker_input, dow_input], outputs=output)
    optimizer = optimizers.Adam(learning_rate=0.0005)
    model.compile(optimizer=optimizer, loss=Huber(), metrics=[RootMeanSquaredError()])

    return model
