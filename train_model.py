# ---- Silence TensorFlow warnings ----
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import pandas as pd
import pickle
import tensorflow as tf

# Safe Keras access
Tokenizer = tf.keras.preprocessing.text.Tokenizer
pad_sequences = tf.keras.preprocessing.sequence.pad_sequences
Sequential = tf.keras.models.Sequential
Embedding = tf.keras.layers.Embedding
LSTM = tf.keras.layers.LSTM
Dense = tf.keras.layers.Dense

# Load dataset
data = pd.read_csv("dataset.csv")

# Text processing
tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
tokenizer.fit_on_texts(data["complaint"])

X = pad_sequences(
    tokenizer.texts_to_sequences(data["complaint"]),
    maxlen=100,
    padding="post",
    truncating="post"
)

# Labels must be integers: 0,1,2
y = data["label"].values

# Model
model = Sequential([
    Embedding(input_dim=5000, output_dim=64),
    LSTM(64),
    Dense(3, activation="softmax")
])

# Compile (modern, correct API)
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Train
model.fit(X, y, epochs=5, batch_size=8)

# Save model & tokenizer
model.save("fraud_model.h5")
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("✅ Model trained and saved successfully")
