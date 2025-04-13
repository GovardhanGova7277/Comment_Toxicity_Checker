import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import pickle

# Load data
df = pd.read_csv('train.csv')
X = df['comment_text'].values
y = df['toxic'].values

# Initialize and fit tokenizer
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(X)

# Convert text to sequences
X_seq = tokenizer.texts_to_sequences(X)
X_pad = pad_sequences(X_seq, maxlen=100)

# Build model
model = Sequential([
    Embedding(10000, 128, input_length=100),
    LSTM(128, return_sequences=True),
    Dropout(0.2),
    LSTM(64),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train model
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
model.fit(X_pad, y, validation_split=0.2, epochs=10, batch_size=32, callbacks=[early_stopping])

# Save model
model.save('lstm_toxicity_model.h5')
print("Model saved successfully")

# Save tokenizer
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
print("Tokenizer saved successfully") 