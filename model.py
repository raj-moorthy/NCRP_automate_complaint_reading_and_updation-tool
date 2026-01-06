# ---- Silence TensorFlow warnings ----
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import pickle
import tensorflow as tf

pad_sequences = tf.keras.preprocessing.sequence.pad_sequences

# Load model & tokenizer
model = tf.keras.models.load_model("fraud_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Label mapping (must match training)
FRAUD_LEVELS = ["Low Risk", "Medium Risk", "High Risk"]

def summarize_text(text):
    sentences = text.split(".")
    return ".".join(sentences[:2])  # short summary


def predict_fraud(text: str):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=100, padding="post", truncating="post")

    pred = model.predict(padded, verbose=0)
    level_index = pred.argmax()

    category = "Cyber Fraud"
    fraud_level = FRAUD_LEVELS[level_index]

    summary = summarize_text(text)
    return category, fraud_level, summary

def generate_summary(text):
    if not text:
        return "Summary unavailable"
    text = text.replace("\n", " ")
    return text[:120] + "..." if len(text) > 120 else text
