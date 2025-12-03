#!/usr/bin/env python3
"""
Single server untuk frontend dan backend
Run: python server.py
Akses: http://localhost:8000
"""

from flask import Flask, request, jsonify, send_from_directory
import pickle
import re
import json
import uuid
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')

# Load models
print("Loading models...")
with open('../outputs/models/tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('../outputs/models/naive_bayes_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../outputs/models/slang_dict.pkl', 'rb') as f:
    slang_dict = pickle.load(f)

with open('../outputs/models/stopwords.pkl', 'rb') as f:
    stopwords = pickle.load(f)

# Load dictionaries
with open('../data/dictionaries/symptoms_dict.json', 'r', encoding='utf-8') as f:
    symptoms_dict = json.load(f)

with open('../data/dictionaries/severity_keywords.json', 'r', encoding='utf-8') as f:
    severity_dict = json.load(f)

with open('../data/dictionaries/location_keywords.json', 'r', encoding='utf-8') as f:
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

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

# API endpoints
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    return jsonify({
        'session_id': 'test-123',
        'bot_message': 'Selamat datang! Saya adalah asisten medis PUSTU. Untuk memulai anamnesis, boleh saya tahu nama lengkap Anda?',
        'state': 'greeting'
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    return jsonify({'message': 'Session reset successful'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'loaded'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Server berjalan di http://localhost:8000")
    print("Buka browser dan akses: http://localhost:8000")
    print("Tekan CTRL+C untuk stop server")
    print("="*60 + "\n")
    app.run(debug=False, port=8000, host='0.0.0.0')
