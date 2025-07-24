from keras.layers import Embedding, Input, LSTM, Dense, Dropout, Concatenate, RepeatVector, Flatten
from keras.models import Model


def build_model(N, num_tickers, num_features, emb_dim=8):

    seq_input = Input(shape=(N, num_features), name='seq_input')
    ticker_input = Input(shape=(1,), name='ticker_input')

    ticker_emb = Embedding(input_dim=num_tickers, output_dim=emb_dim, name='ticker_emb')(ticker_input)
    ticker_emb = Flatten()(ticker_emb)
    ticker_emb = Dropout(0.2)(ticker_emb)

    ticker_repeated = RepeatVector(N)(ticker_emb)
    merged = Concatenate()([seq_input, ticker_repeated])

    x = LSTM(64)(merged)
    x = Dropout(0.2)(x)
    output = Dense(1)(x)

    model = Model(inputs=[seq_input, ticker_input], outputs=output)
    model.compile(optimizer='adam', loss='mse')
    model.summary()
    return model
