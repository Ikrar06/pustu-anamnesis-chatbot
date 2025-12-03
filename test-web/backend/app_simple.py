from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import json
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load models
print("Loading models...")
with open('../../outputs/models/tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('../../outputs/models/naive_bayes_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../../outputs/models/slang_dict.pkl', 'rb') as f:
    slang_dict = pickle.load(f)

with open('../../outputs/models/stopwords.pkl', 'rb') as f:
    stopwords = pickle.load(f)

# Load dictionaries
with open('../../data/dictionaries/symptoms_dict.json', 'r', encoding='utf-8') as f:
    symptoms_dict = json.load(f)

with open('../../data/dictionaries/severity_keywords.json', 'r', encoding='utf-8') as f:
    severity_dict = json.load(f)

with open('../../data/dictionaries/location_keywords.json', 'r', encoding='utf-8') as f:
    location_dict = json.load(f)

print("Models loaded successfully!")

# Store active sessions
sessions = {}

# Preprocessing function
def preprocess(text, slang_dict, stopwords):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    words = [slang_dict.get(w, w) for w in words]
    words = [w for w in words if w not in stopwords]
    return ' '.join(words)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    return jsonify({
        'session_id': 'test-123',
        'bot_message': 'Hello! This is a test response.',
        'state': 'greeting'
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    return jsonify({'message': 'Session reset successful'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'loaded'})

if __name__ == '__main__':
    print("Starting Flask server on port 5000...")
    app.run(debug=False, port=5000, host='0.0.0.0')
