from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# Configure CORS - allow all origins
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

# Comprehensive Entity Extractor
class EntityExtractor:
    """Comprehensive entity extraction for medical anamnesis"""

    def __init__(self, symptoms_dict, severity_dict, location_dict):
        self.symptoms_dict = symptoms_dict
        self.severity_dict = severity_dict
        self.location_dict = location_dict

    def extract_nama(self, text):
        """Extract patient name from text"""
        pattern = r'nama\s+(?:saya\s+)?(\w+(?:\s+\w+)?)'
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1).title()
        return None

    def extract_umur(self, text):
        """Extract age from text"""
        pattern = r'(\d+)\s*(?:tahun|th|thn)'
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
        return None

    def extract_jenis_kelamin(self, text):
        """Extract gender from text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['laki-laki', 'laki', 'pria', 'cowok', 'cowo']):
            return 'Laki-laki'
        elif any(word in text_lower for word in ['perempuan', 'wanita', 'cewek', 'cewe']):
            return 'Perempuan'
        return None

    def extract_durasi(self, text):
        """Extract duration from text (excluding age mentions)"""
        text_lower = text.lower()

        # Pattern 1: Duration with context keywords (prevents "28 tahun" from matching)
        duration_contexts = ['sudah', 'sejak', 'selama', 'sekitar', 'kurang lebih', 'kira-kira',
                           'hampir', 'lebih dari']
        for context in duration_contexts:
            pattern = rf'{context}\s+(\d+)\s*(?:hari|minggu|bulan|tahun|jam|menit)'
            match = re.search(pattern, text_lower)
            if match:
                return match.group(0)

        # Pattern 2: Simple patterns for hari/minggu/bulan (safe without context)
        simple_pattern = r'(\d+)\s*(?:hari|minggu|bulan)'
        match = re.search(simple_pattern, text_lower)
        if match:
            return match.group(0)

        # Pattern 3: Relative time expressions
        relative_pattern = r'sejak\s+(?:kemarin|lusa|seminggu|sebulan|tadi|pagi|siang|sore|malam)'
        match = re.search(relative_pattern, text_lower)
        if match:
            return match.group(0)

        return None

    def extract_lokasi(self, text):
        """Extract body location from text"""
        text_lower = text.lower()
        for location, keywords in self.location_dict.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return location
        return None

    def extract_severity(self, text):
        """Extract severity level from text"""
        text_lower = text.lower()
        for severity, info in self.severity_dict.items():
            for keyword in info['keywords']:
                if keyword in text_lower:
                    return severity
        return None

    def extract_symptoms(self, text):
        """Extract symptoms from text"""
        text_lower = text.lower()
        found_symptoms = []
        for symptom, info in self.symptoms_dict.items():
            if symptom in text_lower:
                found_symptoms.append(symptom)
            for synonym in info.get('synonyms', []):
                if synonym in text_lower and symptom not in found_symptoms:
                    found_symptoms.append(symptom)
        return found_symptoms

    def extract_all(self, text):
        """Extract all entities from text"""
        return {
            'nama': self.extract_nama(text),
            'umur': self.extract_umur(text),
            'jenis_kelamin': self.extract_jenis_kelamin(text),
            'durasi': self.extract_durasi(text),
            'lokasi': self.extract_lokasi(text),
            'severity': self.extract_severity(text),
            'symptoms': self.extract_symptoms(text)
        }

# Initialize entity extractor
extractor = EntityExtractor(symptoms_dict, severity_dict, location_dict)

# Dialog State Manager
class DialogStateManager:
    def __init__(self):
        self.state = 'greeting'
        self.data = {}
        self.retry_count = {}
        self.flow = [
            'greeting', 'nama', 'nama_panggilan', 'umur', 'jenis_kelamin',
            'keluhan_utama', 'gejala', 'durasi',
            'lokasi', 'severity', 'riwayat_penyakit',
            'riwayat_obat', 'alergi', 'faktor_risiko', 'summary'
        ]
        self.questions = {
            'greeting': 'Selamat datang di Chatbot PUSTU. Saya akan membantu mencatat keluhan Anda. Boleh saya tahu nama lengkap Anda?',
            'nama': 'Boleh saya tahu nama lengkap Anda?',
            'nama_panggilan': 'Baik, boleh dipanggil apa?',
            'umur': '{nama}, berapa usia Anda?',
            'jenis_kelamin': 'Jenis kelamin Anda? (laki-laki/perempuan)',
            'keluhan_utama': 'Baik {nama}, sekarang ceritakan keluhan utama yang Anda rasakan.',
            'gejala': 'Apakah ada gejala lain yang menyertai?',
            'durasi': 'Sudah berapa lama {nama} merasakan keluhan ini?',
            'lokasi': 'Di bagian tubuh mana {nama} merasakan keluhan tersebut?',
            'severity': 'Seberapa parah yang Anda rasakan? Ringan, sedang, atau berat?',
            'riwayat_penyakit': '{nama}, apakah Anda memiliki riwayat penyakit sebelumnya?',
            'riwayat_obat': 'Apakah saat ini sedang mengonsumsi obat-obatan?',
            'alergi': 'Apakah {nama} memiliki alergi terhadap makanan atau obat tertentu?',
            'faktor_risiko': 'Apakah ada kebiasaan yang ingin Anda sampaikan? Seperti merokok, kurang olahraga, dll.',
            'summary': 'Terima kasih {nama} atas informasinya. Berikut ringkasan hasil anamnesis Anda:'
        }
        self.retry_messages = {
            'nama': ['Boleh tahu nama lengkap Anda?'],
            'nama_panggilan': ['Boleh dipanggil siapa?'],
            'umur': ['Berapa usia Anda saat ini?'],
            'jenis_kelamin': ['Jenis kelamin Anda laki-laki atau perempuan?'],
            'keluhan_utama': [
                'Bisa ceritakan lagi keluhan utama yang Anda rasakan?',
                'Bisa dijelaskan keluhan yang Anda alami saat ini?'
            ],
            'gejala': [
                'Apakah ada gejala lain yang menyertai?',
                'Selain itu, ada gejala penyerta lainnya?'
            ],
            'durasi': [
                'Sudah berapa lama Anda merasakan keluhan ini? Contoh: 3 hari, 1 minggu',
                'Bisa sebutkan sudah berapa lama mengalami keluhan tersebut?'
            ],
            'lokasi': [
                'Di bagian tubuh mana Anda merasakan keluhan tersebut?',
                'Bisa sebutkan lokasi keluhan yang Anda rasakan?'
            ],
            'severity': [
                'Tingkat keparahannya ringan, sedang, atau berat?',
                'Seberapa parah yang Anda rasakan?'
            ],
            'riwayat_penyakit': [
                'Apakah ada riwayat penyakit sebelumnya? Jika tidak, sebutkan "tidak ada"'
            ],
            'riwayat_obat': [
                'Apakah sedang mengonsumsi obat? Jika tidak, sebutkan "tidak"'
            ],
            'alergi': [
                'Apakah ada alergi terhadap makanan atau obat? Jika tidak, sebutkan "tidak ada"'
            ],
            'faktor_risiko': [
                'Apakah ada kebiasaan tertentu? Seperti merokok, kurang olahraga, dll. Jika tidak, sebutkan "tidak ada"'
            ]
        }

        # Expected intents for each state (jawab_gejala REMOVED - overlaps with other intents)
        self.expected_intents = {
            'nama': [],  # Accept anything
            'nama_panggilan': [],  # Accept anything
            'umur': [],  # Accept anything
            'jenis_kelamin': [],  # Accept anything
            'keluhan_utama': ['keluhan_utama', 'jawab_gejala_penyerta'],
            'gejala': ['jawab_gejala_penyerta', 'keluhan_utama', 'penyangkalan', 'tidak_jelas'],
            'durasi': ['jawab_durasi'],
            'lokasi': ['jawab_lokasi'],
            'severity': ['jawab_severity'],
            'riwayat_penyakit': ['jawab_riwayat_penyakit', 'penyangkalan', 'tidak_jelas'],
            'riwayat_obat': ['jawab_riwayat_obat', 'penyangkalan', 'tidak_jelas'],
            'alergi': ['jawab_alergi', 'penyangkalan', 'tidak_jelas'],
            'faktor_risiko': ['jawab_faktor_risiko', 'penyangkalan', 'tidak_jelas']
        }

    def get_current_question(self, retry=False):
        if retry and self.state in self.retry_messages:
            retry_idx = self.retry_count.get(self.state, 0) % len(self.retry_messages[self.state])
            question = self.retry_messages[self.state][retry_idx]
        else:
            question = self.questions.get(self.state, '')

        # Replace {nama} placeholder with actual name (prefer nickname if available)
        if '{nama}' in question:
            if 'nama_panggilan' in self.data:
                # Use nickname
                nama = self.data['nama_panggilan']['message'].strip()
                nama = re.sub(r'^(panggil\s+)?', '', nama, flags=re.IGNORECASE).strip()
                if nama:
                    nama = nama.title()
            elif 'nama' in self.data:
                # Use first name only from full name
                nama = self.data['nama']['message'].strip()
                nama = re.sub(r'^(saya|nama\s+saya|nama)\s+', '', nama, flags=re.IGNORECASE).strip()
                # Take only first name
                nama = nama.split()[0] if nama else ''
                if nama:
                    nama = nama.title()
            else:
                nama = ''

            question = question.replace('{nama}', nama)

        return question

    def get_next_state(self):
        current_idx = self.flow.index(self.state)
        if current_idx < len(self.flow) - 1:
            return self.flow[current_idx + 1]
        return 'summary'

    def is_intent_valid(self, intent):
        """Check if intent matches expected intent for current state"""
        if self.state not in self.expected_intents:
            return True
        # Empty list means accept anything
        if not self.expected_intents[self.state]:
            return True
        return intent in self.expected_intents[self.state]

    def update(self, intent, user_message, entities, is_valid):
        if is_valid:
            # Store data
            self.data[self.state] = {
                'message': user_message,
                'intent': intent,
                'entities': entities
            }
            # Reset retry count for this state
            self.retry_count[self.state] = 0
            # Move to next state
            self.state = self.get_next_state()
            return True
        else:
            # Increment retry count
            self.retry_count[self.state] = self.retry_count.get(self.state, 0) + 1
            return False

    def smart_prefill(self, user_message, entities):
        """Auto-fill future states if user already provided the information"""
        # This is called AFTER state update, so check if we haven't passed these states yet
        current_idx = self.flow.index(self.state)

        # Check if user provided duration info and we haven't reached durasi state yet
        if entities.get('durasi') and 'durasi' not in self.data:
            durasi_idx = self.flow.index('durasi')
            if current_idx <= durasi_idx:
                self.data['durasi'] = {
                    'message': entities['durasi'],
                    'intent': 'jawab_durasi',
                    'entities': entities
                }

        # Check if user provided location info and we haven't reached lokasi state yet
        if entities.get('lokasi') and 'lokasi' not in self.data:
            lokasi_idx = self.flow.index('lokasi')
            if current_idx <= lokasi_idx:
                self.data['lokasi'] = {
                    'message': f"di {entities['lokasi']}",
                    'intent': 'jawab_lokasi',
                    'entities': entities
                }

        # Check if user provided severity info and we haven't reached severity state yet
        if entities.get('severity') and 'severity' not in self.data:
            severity_idx = self.flow.index('severity')
            if current_idx <= severity_idx:
                self.data['severity'] = {
                    'message': entities['severity'],
                    'intent': 'jawab_severity',
                    'entities': entities
                }

        # Check if user provided symptoms info (but DON'T auto-fill gejala from keluhan_utama)
        # Only backfill gejala if we're past it but still in early states (before riwayat)
        if entities.get('symptoms') and 'gejala' not in self.data:
            gejala_idx = self.flow.index('gejala')
            riwayat_idx = self.flow.index('riwayat_penyakit')

            # Only prefill if we're in durasi/lokasi/severity states (after gejala but before riwayat)
            # Don't prefill from keluhan_utama state (user will be asked properly)
            if gejala_idx < current_idx <= riwayat_idx and len(entities['symptoms']) > 0:
                self.data['gejala'] = {
                    'message': ', '.join(entities['symptoms']),
                    'intent': 'jawab_gejala_penyerta',
                    'entities': entities
                }

    def skip_filled_states(self):
        """Skip states that have already been filled by smart prefill"""
        max_skips = 5  # Prevent infinite loops
        skipped = 0
        while self.state in self.data and self.state != 'summary' and skipped < max_skips:
            self.state = self.get_next_state()
            skipped += 1

    def get_summary(self):
        summary = []

        # Patient Identity Section
        identity_section = []

        # Process nama
        if 'nama' in self.data:
            nama = self.data['nama']['message'].strip()
            nama = re.sub(r'^(saya|nama\s+saya|nama)\s+', '', nama, flags=re.IGNORECASE).strip()
            nama = nama.title() if nama else ""
            identity_section.append(f"Nama          : {nama}")
            patient_name = nama
        else:
            patient_name = ""

        # Process umur
        if 'umur' in self.data:
            umur = self.data['umur']['message'].strip()
            umur = re.sub(r'^(saya|aku)\s+', '', umur, flags=re.IGNORECASE)
            # Ensure "tahun" is present
            if not re.search(r'tahun', umur, flags=re.IGNORECASE):
                umur = f"{umur} tahun"
            identity_section.append(f"Usia          : {umur}")

        # Process jenis_kelamin
        if 'jenis_kelamin' in self.data:
            gender = self.data['jenis_kelamin']['message'].strip().lower()
            # Normalize gender format
            if 'laki' in gender or 'pria' in gender or 'cowok' in gender:
                gender = 'Laki-laki'
            elif 'perempuan' in gender or 'wanita' in gender or 'cewek' in gender:
                gender = 'Perempuan'
            else:
                gender = gender.capitalize()
            identity_section.append(f"Jenis Kelamin : {gender}")

        if identity_section:
            summary.append("=" * 60)
            summary.append("IDENTITAS PASIEN")
            summary.append("=" * 60)
            summary.extend(identity_section)
            summary.append("")

        # Medical History Section
        summary.append("ANAMNESIS")
        summary.append("-" * 60)

        # Process each medical field
        medical_data = []

        # Keluhan Utama - remove duration if present
        if 'keluhan_utama' in self.data:
            message = self.data['keluhan_utama']['message'].strip()
            message = re.sub(r'^(saya|aku)\s+', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+(dokter|dok|bu|pak|mas|mbak|kak)\s*', ' ', message, flags=re.IGNORECASE)
            # Remove duration patterns - both with and without context words
            # Pattern 1: "sudah/sejak/selama X hari"
            message = re.sub(r'\s*(sudah|sejak|selama|sekitar|kurang lebih)\s+\d+\s*(hari|minggu|bulan|tahun|jam|menit)', '', message, flags=re.IGNORECASE)
            # Pattern 2: "X hari" (standalone duration at end)
            message = re.sub(r'\s+\d+\s*(hari|minggu|bulan|tahun|jam|menit)\s*$', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+', ' ', message).strip()
            message = message.capitalize() if message else message
            medical_data.append(f"Keluhan Utama       : {message}")

        # Gejala Penyerta - convert to professional terminology
        if 'gejala' in self.data:
            message = self.data['gejala']['message'].strip()
            message = re.sub(r'^(saya|aku)\s+', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+(saya|aku)\s+', ' ', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+(dokter|dok|bu|pak|mas|mbak|kak)\s*', ' ', message, flags=re.IGNORECASE)
            # Convert informal to formal: "juga", "sekali", etc. (use word boundaries)
            message = re.sub(r'\b(juga|sekali|banget)\b', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+', ' ', message).strip()
            # Professional terminology
            message = re.sub(r'\bsakit kepala\b', 'nyeri kepala', message, flags=re.IGNORECASE)
            message = re.sub(r'\bsakit\b', 'nyeri', message, flags=re.IGNORECASE)
            message = message.capitalize() if message else message
            medical_data.append(f"Gejala Penyerta     : {message}")

        # Durasi
        if 'durasi' in self.data:
            message = self.data['durasi']['message'].strip()
            message = message.capitalize() if message else message
            medical_data.append(f"Durasi              : {message}")

        # Lokasi - remove "di" prefix
        if 'lokasi' in self.data:
            message = self.data['lokasi']['message'].strip()
            message = re.sub(r'^di\s+', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+(dokter|dok|bu|pak|mas|mbak|kak)\s*', ' ', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+', ' ', message).strip()
            message = message.capitalize() if message else message
            medical_data.append(f"Lokasi              : {message}")

        # Severity - professional terminology
        if 'severity' in self.data:
            severity_map = {
                'ringan': 'Ringan',
                'sedang': 'Sedang',
                'berat': 'Berat',
                'parah': 'Berat',
                'sangat': 'Berat'
            }
            message = self.data['severity']['message'].strip().lower()
            for key, value in severity_map.items():
                if key in message:
                    message = value
                    break
            medical_data.append(f"Tingkat Keparahan   : {message}")

        summary.extend(medical_data)
        summary.append("")

        # Medical history section
        summary.append("RIWAYAT MEDIS")
        summary.append("-" * 60)

        history_data = []

        # Riwayat Penyakit
        if 'riwayat_penyakit' in self.data:
            message = self.data['riwayat_penyakit']['message'].strip()
            message = re.sub(r'^(saya|aku)\s+', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+(dokter|dok|bu|pak|mas|mbak|kak)\s*', ' ', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+', ' ', message).strip()
            negation = ['tidak', 'tidak ada', 'tidak tahu', 'ga', 'gak', 'enggak', 'nggak']
            if any(message.lower().startswith(neg) for neg in negation):
                message = 'Tidak ada'
            else:
                message = message.capitalize() if message else message
            history_data.append(f"Riwayat Penyakit    : {message}")

        # Riwayat Obat
        if 'riwayat_obat' in self.data:
            message = self.data['riwayat_obat']['message'].strip()
            message = re.sub(r'^(saya|aku)\s+', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+(dokter|dok|bu|pak|mas|mbak|kak)\s*', ' ', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+', ' ', message).strip()
            negation = ['tidak', 'tidak ada', 'tidak tahu', 'ga', 'gak', 'enggak', 'nggak']
            if any(message.lower().startswith(neg) for neg in negation):
                message = 'Tidak ada'
            else:
                message = message.capitalize() if message else message
            history_data.append(f"Obat yang Dikonsumsi : {message}")

        # Alergi
        if 'alergi' in self.data:
            message = self.data['alergi']['message'].strip()
            message = re.sub(r'^(saya|aku)\s+', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+(dokter|dok|bu|pak|mas|mbak|kak)\s*', ' ', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+', ' ', message).strip()
            negation = ['tidak', 'tidak ada', 'tidak tahu', 'ga', 'gak', 'enggak', 'nggak']
            if any(message.lower().startswith(neg) for neg in negation):
                message = 'Tidak ada'
            else:
                message = message.capitalize() if message else message
            history_data.append(f"Riwayat Alergi      : {message}")

        # Faktor Risiko
        if 'faktor_risiko' in self.data:
            message = self.data['faktor_risiko']['message'].strip()
            message = re.sub(r'^(saya|aku)\s+', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+(dokter|dok|bu|pak|mas|mbak|kak)\s*', ' ', message, flags=re.IGNORECASE)
            message = re.sub(r'\s+', ' ', message).strip()
            negation = ['tidak', 'tidak ada', 'tidak tahu', 'ga', 'gak', 'enggak', 'nggak']
            if any(message.lower().startswith(neg) for neg in negation):
                message = 'Tidak ada'
            else:
                message = message.capitalize() if message else message
            history_data.append(f"Faktor Risiko       : {message}")

        summary.extend(history_data)
        summary.append("=" * 60)

        return "\n".join(summary)

# Predict intent with keyword boost
def predict_intent(text):
    processed = preprocess(text, slang_dict, stopwords)
    tfidf = vectorizer.transform([processed])
    pred = model.predict(tfidf)[0]
    proba = model.predict_proba(tfidf)[0]
    confidence = float(max(proba))

    # Use comprehensive entity extractor
    all_entities = extractor.extract_all(text)
    location = all_entities['lokasi']
    durasi = all_entities['durasi']
    severity = all_entities['severity']

    # Keyword-based intent boosting (override model if keywords strongly match)
    text_lower = text.lower()

    # Duration keywords - use extractor result
    if durasi:  # If extractor found duration with proper context
        pred = 'jawab_durasi'
        confidence = 0.95

    # Severity keywords
    elif severity:  # If extractor found severity
        if confidence < 0.7:  # Only override if model is uncertain
            pred = 'jawab_severity'
            confidence = 0.90

    # Location - if entity detected and mentions body parts
    elif location and any(kw in text_lower for kw in ['di', 'bagian', 'sebelah', 'area']):
        pred = 'jawab_lokasi'
        confidence = 0.90

    # Allergy keywords
    elif any(kw in text_lower for kw in ['alergi', 'bentol', 'gatal', 'ruam']) and 'alergi' in text_lower:
        pred = 'jawab_alergi'
        confidence = 0.90

    return {
        'intent': pred,
        'confidence': confidence,
        'entities': all_entities,
        'location': location,
        'processed': processed
    }

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id')

    # Create or get session
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = DialogStateManager()

    dsm = sessions[session_id]

    # Handle initial greeting state
    if dsm.state == 'greeting':
        response = {
            'session_id': session_id,
            'bot_message': dsm.get_current_question(),
            'state': dsm.state
        }
        dsm.state = 'nama'  # Move to nama collection, not keluhan_utama
        return jsonify(response)

    # Predict intent
    result = predict_intent(user_message)
    predicted_intent = result['intent']

    # Handle greetings and politeness naturally (don't break flow)
    greeting_keywords = ['halo', 'hai', 'assalamualaikum', 'selamat', 'permisi']
    is_greeting = any(kw in user_message.lower() for kw in greeting_keywords)

    if is_greeting or predicted_intent in ['sapaan', 'ucapan_terima_kasih']:
        if is_greeting or predicted_intent == 'sapaan':
            if 'assalamualaikum' in user_message.lower():
                greeting = 'Waalaikumsalam. '
            else:
                greeting = 'Halo! '
            bot_message = greeting + 'Saya chatbot PUSTU yang akan membantu Anda. ' + dsm.get_current_question()
        else:
            bot_message = 'Sama-sama! Mari kita lanjutkan. ' + dsm.get_current_question()

        response = {
            'session_id': session_id,
            'intent': predicted_intent,
            'confidence': result['confidence'],
            'entities': result['entities'],
            'location': result['location'],
            'bot_message': bot_message,
            'state': dsm.state
        }
        return jsonify(response)

    # Handle "tidak tahu" / "tidak jelas" responses - accept and move on
    uncertainty_keywords = ['tidak tahu', 'tidak tau', 'kurang tahu', 'tidak jelas', 'tidak yakin', 'kurang jelas']
    is_uncertain = any(kw in user_message.lower() for kw in uncertainty_keywords)

    if is_uncertain or predicted_intent == 'tidak_jelas':
        # User doesn't know - accept it and move on
        is_valid = True
        state_changed = dsm.update(predicted_intent, user_message, result['entities'], is_valid)
    else:
        # Special handling for keluhan_utama (user might mention symptoms + duration/location together)
        if dsm.state == 'keluhan_utama':
            # Check if message contains symptom keywords
            symptom_keywords = ['demam', 'sakit', 'pusing', 'mual', 'batuk', 'flu', 'muntah', 'diare', 'gatal']
            has_symptom = any(kw in user_message.lower() for kw in symptom_keywords)
            if has_symptom:
                # Accept it regardless of predicted intent
                is_valid = True
                predicted_intent = 'keluhan_utama'
            else:
                is_valid = dsm.is_intent_valid(predicted_intent)

        # Special handling for gejala state (check for symptom keywords)
        elif dsm.state == 'gejala':
            # Check if message contains symptom keywords
            symptom_keywords = ['sakit', 'nyeri', 'pusing', 'mual', 'muntah', 'diare', 'batuk',
                               'pilek', 'demam', 'lemas', 'panas', 'dingin', 'menggigil',
                               'sesak', 'gatal', 'bengkak', 'kram', 'kaku', 'berdarah']
            has_symptom = any(kw in user_message.lower() for kw in symptom_keywords)
            if has_symptom:
                # Accept it regardless of predicted intent
                is_valid = True
                predicted_intent = 'jawab_gejala_penyerta'
            else:
                is_valid = dsm.is_intent_valid(predicted_intent)

        # Special handling for severity state (often misclassified)
        elif dsm.state == 'severity':
            severity_keywords = ['ringan', 'sedang', 'berat', 'parah', 'sangat']
            has_severity = any(kw in user_message.lower() for kw in severity_keywords)
            if has_severity:
                # Force validation to pass if severity keyword detected
                is_valid = True
                predicted_intent = 'jawab_severity'
            else:
                is_valid = dsm.is_intent_valid(predicted_intent)

        # Special handling for duration (improve detection)
        elif dsm.state == 'durasi':
            # Check for duration patterns
            duration_pattern = r'\d+\s*(hari|minggu|bulan|tahun|jam|menit)'
            has_duration = re.search(duration_pattern, user_message.lower())
            if has_duration:
                is_valid = True
                predicted_intent = 'jawab_durasi'
            else:
                is_valid = dsm.is_intent_valid(predicted_intent)

        # Special handling for location
        elif dsm.state == 'lokasi':
            # Check if any body part mentioned
            if result['location']:
                is_valid = True
                predicted_intent = 'jawab_lokasi'
            else:
                is_valid = dsm.is_intent_valid(predicted_intent)

        else:
            # Check if intent matches expected intent for current state
            is_valid = dsm.is_intent_valid(predicted_intent)

        # Update dialog state
        state_changed = dsm.update(predicted_intent, user_message, result['entities'], is_valid)

        # Smart prefill: auto-fill future states if user already provided info
        if state_changed:
            dsm.smart_prefill(user_message, result['entities'])
            dsm.skip_filled_states()

        # Limit retries to 1 time only (don't be too pushy)
        if not state_changed and dsm.retry_count.get(dsm.state, 0) >= 2:
            # After 2 retries, force accept and move on
            is_valid = True
            state_changed = dsm.update(predicted_intent, user_message, result['entities'], is_valid)
            if state_changed:
                dsm.smart_prefill(user_message, result['entities'])
                dsm.skip_filled_states()

    # Generate response
    if not state_changed:
        # Intent tidak sesuai, tanya ulang dengan variasi
        bot_message = dsm.get_current_question(retry=True)
    elif dsm.state == 'summary':
        bot_message = dsm.get_current_question() + "\n\n" + dsm.get_summary()
    else:
        bot_message = dsm.get_current_question()

    response = {
        'session_id': session_id,
        'intent': predicted_intent,
        'confidence': result['confidence'],
        'entities': result['entities'],
        'location': result['location'],
        'bot_message': bot_message,
        'state': dsm.state,
        'is_valid': is_valid
    }

    return jsonify(response)

@app.route('/api/reset', methods=['POST'])
def reset():
    data = request.json
    session_id = data.get('session_id')

    if session_id and session_id in sessions:
        del sessions[session_id]

    return jsonify({'message': 'Session reset successful'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'loaded'})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
