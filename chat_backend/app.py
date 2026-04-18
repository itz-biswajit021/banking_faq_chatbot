# app.py
# -----------------------------------------
# Banking FAQ Chatbot Backend (Intent + FAQ Retrieval)
# -----------------------------------------

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
import json
import os
import logging

from tensorflow.keras.models import load_model
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------------------
# Paths & Config
# -----------------------------------------
MODEL_PATH = "model2/chatbot_model.h5"
TOKENIZER_PATH = "model2/tokenizer.pkl"        # sklearn TfidfVectorizer
ENCODER_PATH = "model2/label_encoder.pkl"      # sklearn LabelEncoder
INTENTS_PATH = "data/bank_faq_intents.json"
FAQ_PATH = "data/BankFAQs.csv"

# Set these to match your CSV column names
QUESTION_COL = "Question"   # e.g. "Question" or "question"
ANSWER_COL = "Answer"       # e.g. "Answer" or "answer"

# Thresholds (tune these based on your data)
CONF_THRESH = 0.70          # min confidence to trust intent classifier
SIM_STRONG = 0.60           # strong FAQ match
SIM_WEAK = 0.30             # weak but usable FAQ match

# -----------------------------------------
# Basic validation of file paths
# -----------------------------------------
for path, label in [
    (MODEL_PATH, "Model"),
    (TOKENIZER_PATH, "Tokenizer"),
    (ENCODER_PATH, "Label encoder"),
    (INTENTS_PATH, "Intents JSON"),
    (FAQ_PATH, "FAQ CSV"),
]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{label} not found at {path}")

# -----------------------------------------
# Logging setup
# -----------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------------------
# Load ML model, tokenizer, label encoder
# -----------------------------------------
logger.info("Loading model and preprocessing tools...")
model = load_model(MODEL_PATH)
tokenizer = joblib.load(TOKENIZER_PATH)
lbl_encoder = joblib.load(ENCODER_PATH)

# Load intents JSON
with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    intents_data = json.load(f)

# -----------------------------------------
# Load FAQ CSV & precompute TF-IDF vectors
# -----------------------------------------
logger.info("Loading FAQ data from CSV...")
faq_df = pd.read_csv(FAQ_PATH)

if QUESTION_COL not in faq_df.columns or ANSWER_COL not in faq_df.columns:
    raise ValueError(
        f"Configured QUESTION_COL='{QUESTION_COL}' or ANSWER_COL='{ANSWER_COL}' "
        f"not found in CSV columns: {faq_df.columns.tolist()}"
    )

faq_questions = faq_df[QUESTION_COL].astype(str).tolist()
faq_answers = faq_df[ANSWER_COL].astype(str).tolist()

# Precompute TF-IDF vectors for all FAQ questions
logger.info("Computing FAQ TF-IDF vectors...")
faq_vectors = tokenizer.transform(faq_questions)

logger.info("Backend initialization complete.")

# -----------------------------------------
# Helper functions
# -----------------------------------------
def classify_intent(message: str):
    """
    Run the intent classifier on a single message.
    Returns: (predicted_tag, confidence, raw_probs_array)
    """
    vec = tokenizer.transform([message])
    probs = model.predict(vec.toarray())[0]  # shape: (num_classes,)
    confidence = float(np.max(probs))
    predicted_index = int(np.argmax(probs))
    predicted_tag = lbl_encoder.inverse_transform([predicted_index])[0]
    return predicted_tag, confidence, probs, vec


def get_intent_response(tag: str) -> str:
    """
    Pick a random response from intents JSON for given tag.
    Returns default message if tag not found.
    """
    for intent in intents_data.get("intents", []):
        if intent.get("tag") == tag:
            if intent.get("responses"):
                return str(np.random.choice(intent["responses"]))
    return "I'm not sure how to respond to that."


def retrieve_faq_answer(vec):
    """
    Retrieve the closest FAQ using cosine similarity.
    Returns: (best_answer, best_score, best_question)
    """
    sims = cosine_similarity(vec, faq_vectors)[0]   # shape: (num_faqs,)
    best_idx = int(np.argmax(sims))
    best_score = float(sims[best_idx])
    best_answer = faq_answers[best_idx]
    best_question = faq_questions[best_idx]
    return best_answer, best_score, best_question


def clean_response(text: str) -> str:
    """
    Clean unwanted substrings from response.
    """
    if not isinstance(text, str):
        text = str(text)
    text = text.replace("View more", "")
    return text.strip()


# -----------------------------------------
# Flask App
# -----------------------------------------
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/", methods=["GET"])
def health():
    """
    Simple health-check / metadata endpoint.
    """
    return jsonify({
        "status": "ok",
        "message": "Bank FAQ chatbot backend is running.",
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True, silent=True) or {}
        message = str(data.get("message", "")).strip()

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # ---------------------------
        # 1) Intent classification
        # ---------------------------
        predicted_tag, confidence, probs, vec = classify_intent(message)

        # ---------------------------
        # 2) FAQ retrieval
        # ---------------------------
        faq_answer, best_score, faq_question = retrieve_faq_answer(vec)

        logger.info(
            "User: %r | intent=%s (%.3f) | faq_sim=%.3f",
            message, predicted_tag, confidence, best_score
        )

        # ---------------------------
        # 3) Decision logic
        # ---------------------------
        response = None
        source = None

        # Prefer FAQ when similarity is very strong
        if best_score >= SIM_STRONG:
            response = faq_answer
            source = "faq_strong"

        # Else, if classifier is confident, use intents.json
        elif confidence >= CONF_THRESH:
            response = get_intent_response(predicted_tag)
            source = "intent"

        # Else, classifier is weak but FAQ has some similarity
        elif best_score >= SIM_WEAK:
            response = faq_answer
            source = "faq_weak"

        # Else, everything is weak → safe fallback
        if response is None:
            response = (
                "I'm not completely sure about that. "
                "Could you rephrase your question about your account, card, loan, or balance?"
            )
            source = "fallback"

        response = clean_response(response)

        return jsonify({
            "intent": predicted_tag,
            "confidence": confidence,
            "similarity": best_score,
            "source": source,
            "matched_faq_question": faq_question if source.startswith("faq") else None,
            "reply": response,
        })

    except Exception as e:
        logger.exception("Backend Error in /chat: %s", e)
        return jsonify({"reply": "Internal server error"}), 500


# -----------------------------------------
# Run App (for local dev)
# -----------------------------------------
if __name__ == "__main__":
    # For production, use gunicorn/uwsgi instead of app.run
    debug_mode = os.getenv("FLASK_DEBUG", "1") == "1"
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
