# Chatbot PUSTU - Sistem Anamnesis Pasien dengan NLP

Chatbot untuk membantu proses anamnesis pasien di Puskesmas Pembantu menggunakan Natural Language Processing dan Naive Bayes Classifier.

## Deskripsi Proyek

Proyek ini adalah aplikasi chatbot berbasis web yang membantu tenaga medis melakukan anamnesis (pengumpulan informasi medis) pasien secara otomatis. Chatbot menggunakan teknik NLP untuk memahami keluhan pasien dan mengekstrak informasi penting seperti gejala, durasi, lokasi, dan tingkat keparahan.

## Fitur Utama

- Dialog interaktif untuk mengumpulkan data pasien
- Ekstraksi otomatis informasi medis dari teks pasien
- Klasifikasi intent menggunakan Naive Bayes
- Ekstraksi entitas (nama, umur, gejala, lokasi, durasi, severity)
- Web interface responsif dengan dark/light mode
- Export hasil anamnesis ke PDF
- Backend API dengan Flask
- Frontend modern dengan Next.js 14

## Teknologi yang Digunakan

### Backend
- Python 3.x
- Flask - Web framework
- Scikit-learn - Machine learning (Naive Bayes, TF-IDF)
- Pandas - Data processing
- NumPy - Numerical operations
- Flask-CORS - Cross-origin resource sharing

### Frontend
- Next.js 14 - React framework
- TypeScript - Type safety
- Tailwind CSS v4 - Styling
- Axios - HTTP client
- jsPDF - PDF generation

## Struktur Proyek

```
NLP_CHATBOT/
├── chatbot-web/              # Aplikasi web
│   ├── backend/              # Flask API server
│   │   ├── app.py           # Main application
│   │   ├── data/            # Dictionary dan dataset
│   │   ├── outputs/         # Model dan hasil training
│   │   └── requirements.txt # Python dependencies
│   └── frontend/            # Next.js application
│       ├── app/             # Next.js app router
│       ├── components/      # React components
│       ├── hooks/           # Custom React hooks
│       ├── lib/             # Utility functions
│       └── package.json     # Node dependencies
├── data/                    # Dataset dan dictionary
│   ├── dictionaries/        # Kamus gejala, lokasi, severity
│   ├── processed/           # Data yang sudah diproses
│   └── raw/                 # Data mentah
├── outputs/                 # Hasil training dan visualisasi
│   ├── models/              # Model yang sudah dilatih
│   └── figures/             # Grafik evaluasi
├── pustu_chatbot_training.ipynb  # Notebook untuk training
└── README.md               # Dokumentasi ini
```

## Cara Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd NLP_CHATBOT
```

### 2. Setup Backend

```bash
cd chatbot-web/backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Jalankan server
python app.py
```

Backend akan berjalan di `http://localhost:5000`

### 3. Setup Frontend

```bash
cd chatbot-web/frontend

# Install dependencies
npm install

# Jalankan development server
npm run dev
```

Frontend akan berjalan di `http://localhost:3000`

## Cara Menggunakan

### Training Model

1. Buka `pustu_chatbot_training.ipynb` dengan Jupyter Notebook
2. Jalankan semua cell secara berurutan
3. Model akan disimpan di folder `chatbot-web/backend/outputs/models/`

### Menjalankan Aplikasi Web

1. Pastikan backend sudah berjalan di port 5000
2. Pastikan frontend sudah berjalan di port 3000
3. Buka browser dan akses `http://localhost:3000`
4. Mulai chat dengan mengikuti instruksi chatbot
5. Setelah selesai, download hasil anamnesis dalam format PDF

### Alur Anamnesis

Chatbot akan menanyakan informasi dalam urutan berikut:

1. Nama lengkap
2. Nama panggilan
3. Usia
4. Jenis kelamin
5. Keluhan utama
6. Gejala penyerta
7. Durasi keluhan
8. Lokasi keluhan
9. Tingkat keparahan
10. Riwayat penyakit
11. Obat yang dikonsumsi
12. Riwayat alergi
13. Faktor risiko

## Deployment

### Deploy Backend ke Railway

1. Login ke Railway: `https://railway.app`
2. Connect dengan GitHub
3. Import repository ini
4. Set root directory: `chatbot-web/backend`
5. Railway akan auto-deploy menggunakan Procfile

### Deploy Frontend ke Vercel

1. Login ke Vercel: `https://vercel.com`
2. Connect dengan GitHub
3. Import repository ini
4. Set root directory: `chatbot-web/frontend`
5. Tambahkan environment variable:
   - `NEXT_PUBLIC_API_URL`: URL backend dari Railway


## Konfigurasi

### Environment Variables

**Backend** (`.env` di folder backend):
```
FLASK_ENV=production
FLASK_DEBUG=False
```

**Frontend** (`.env.local` di folder frontend):
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

Untuk production, ganti URL dengan URL backend yang sudah di-deploy.

## Dataset dan Intent

Dataset anamnesis dibuat menggunakan kombinasi:
- Data sintetis dari panduan medis
- Variasi bahasa Indonesia natural
- Normalisasi slang dan bahasa informal

### Intent yang Digunakan

Model chatbot menggunakan 14 intent untuk klasifikasi dialog:

| Intent | Deskripsi | Contoh |
|--------|-----------|--------|
| `sapaan` | Sapaan awal dari pasien | "Halo dok", "Selamat pagi" |
| `keluhan_utama` | Keluhan utama pasien | "Saya sakit kepala", "Demam tinggi" |
| `jawab_gejala_penyerta` | Gejala tambahan yang menyertai | "Ada mual juga", "Batuk pilek" |
| `jawab_durasi` | Lama waktu keluhan dirasakan | "Sudah 3 hari", "Sejak kemarin" |
| `jawab_lokasi` | Lokasi keluhan di tubuh | "Di kepala bagian kanan", "Perut" |
| `jawab_severity` | Tingkat keparahan keluhan | "Ringan", "Parah sekali" |
| `jawab_riwayat_penyakit` | Riwayat penyakit sebelumnya | "Pernah tipes", "Tidak ada" |
| `jawab_riwayat_obat` | Obat yang sedang dikonsumsi | "Paracetamol", "Tidak ada" |
| `jawab_alergi` | Alergi makanan atau obat | "Alergi seafood", "Tidak ada" |
| `jawab_faktor_risiko` | Kebiasaan dan faktor risiko | "Merokok", "Kurang olahraga" |
| `konfirmasi` | Konfirmasi atau persetujuan | "Ya", "Benar", "Iya dok" |
| `penyangkalan` | Jawaban negatif | "Tidak", "Tidak ada" |
| `tidak_jelas` | Jawaban tidak tahu/tidak jelas | "Tidak tahu", "Kurang yakin" |
| `ucapan_terima_kasih` | Ucapan terima kasih | "Terima kasih", "Makasih dok" |

### Distribusi Intent dalam Dataset

![Intent Distribution](outputs/figures/intent_distribution.png)

*Gambar: Distribusi jumlah sampel untuk setiap intent dalam dataset training*

## Pendekatan NLP dan Machine Learning

### NLP dari Scratch (Tanpa Framework Besar)

Proyek ini menggunakan pendekatan **NLP dari scratch** tanpa library besar seperti spaCy, NLTK advanced, atau Transformers. Semua preprocessing dan entity extraction dibuat manual menggunakan:

**1. Text Preprocessing Manual**
```python
def preprocess(text, slang_dict, stopwords):
    text = text.lower()                    # Lowercase
    text = re.sub(r'[^\w\s]', ' ', text)  # Hapus punctuation
    words = text.split()
    words = [slang_dict.get(w, w) for w in words]  # Normalisasi slang
    words = [w for w in words if w not in stopwords]  # Hapus stopwords
    return ' '.join(words)
```

**2. Custom Dictionary untuk NER (Named Entity Recognition)**

Sistem menggunakan dictionary buatan sendiri di folder `data/dictionaries/`:

| File | Deskripsi | Jumlah Entry |
|------|-----------|--------------|
| `symptoms_dict.json` | Daftar gejala medis dengan sinonimnya | 97 gejala |
| `location_keywords.json` | Lokasi keluhan di tubuh | 23 lokasi |
| `severity_keywords.json` | Tingkat keparahan (ringan/sedang/berat) | 3 kategori |
| `slang_normalization.json` | Normalisasi bahasa gaul ke formal | 98 kata |
| `stopwords_id.txt` | Stopwords Bahasa Indonesia | 93 kata |

**3. Regex-based Entity Extraction**

Ekstraksi entitas dilakukan dengan pattern matching manual:
- Durasi: `r'(\d+)\s*(hari|minggu|bulan)'`
- Umur: `r'(\d+)\s*(?:tahun|th|thn)'`
- Nama: `r'nama\s+(?:saya\s+)?(\w+(?:\s+\w+)?)'`
- Gender: Pattern matching dengan keyword list

**Keuntungan Pendekatan Ini:**
- Lebih ringan dan cepat (tidak perlu load model NLP besar)
- Kontrol penuh atas setiap langkah preprocessing
- Mudah di-customize untuk domain medis Indonesia
- Tidak memerlukan GPU untuk inference
- Cocok untuk deployment di resource terbatas

### Machine Learning Library

Untuk klasifikasi intent, proyek ini menggunakan **Scikit-learn**:

**Library yang Digunakan:**
- `scikit-learn` - Machine learning (Naive Bayes, TF-IDF, metrics)
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `matplotlib` - Visualisasi hasil training

**Algoritma dan Teknik:**
- **Algorithm**: Multinomial Naive Bayes dari `sklearn.naive_bayes`
- **Vectorizer**: TfidfVectorizer dari `sklearn.feature_extraction.text`
- **Features**: Unigrams dan bigrams
- **Metrics**: `classification_report`, `confusion_matrix` dari `sklearn.metrics`

**Hyperparameters:**
- TF-IDF max_features: 1000
- N-gram range: (1, 2) - unigrams dan bigrams
- Naive Bayes alpha: 0.1 (Laplace smoothing)

### Hasil Training Model

Model telah dilatih dengan dataset yang mencakup 14 intent berbeda. Berikut adalah hasil evaluasi model:

#### Confusion Matrix

![Confusion Matrix](outputs/figures/confusion_matrix.png)

*Gambar: Confusion matrix menunjukkan performa model dalam memprediksi setiap intent. Diagonal yang lebih gelap menunjukkan prediksi yang benar.*

**Interpretasi:**
- Matriks menunjukkan akurasi tinggi untuk sebagian besar intent
- Intent `keluhan_utama` dan `jawab_gejala_penyerta` memiliki akurasi terbaik
- Beberapa intent seperti `penyangkalan` dan `tidak_jelas` kadang tumpang tindih karena konteks yang mirip

**Metrik Evaluasi:**
- Akurasi keseluruhan: **93%**
- Precision rata-rata: **0.93**
- Recall rata-rata: **0.93**
- F1-score rata-rata: **0.93**

**Performa per Intent:**

| Intent | Precision | Recall | F1-Score | Samples |
|--------|-----------|--------|----------|---------|
| sapaan | 0.98 | 0.98 | 0.98 | 200 |
| keluhan_utama | 0.82 | 0.87 | 0.84 | 200 |
| jawab_gejala_penyerta | 0.90 | 0.90 | 0.90 | 200 |
| jawab_durasi | 0.92 | 0.94 | 0.93 | 200 |
| jawab_lokasi | 0.93 | 0.96 | 0.95 | 200 |
| jawab_severity | 0.91 | 0.88 | 0.89 | 200 |
| jawab_riwayat_penyakit | 0.87 | 0.90 | 0.88 | 200 |
| jawab_riwayat_obat | 0.97 | 0.99 | 0.98 | 200 |
| jawab_alergi | 0.87 | 0.97 | 0.92 | 200 |
| jawab_faktor_risiko | 0.98 | 0.84 | 0.91 | 200 |
| konfirmasi | 0.97 | 0.84 | 0.90 | 200 |
| penyangkalan | 0.98 | 0.95 | 0.96 | 200 |
| tidak_jelas | 0.97 | 0.96 | 0.97 | 200 |
| ucapan_terima_kasih | 0.94 | 0.97 | 0.96 | 200 |

### Entity Extraction (Custom Implementation)

Sistem entity extraction dibuat dari scratch tanpa menggunakan library NER seperti spaCy atau Stanza:

**Teknik yang Digunakan:**

1. **Regex-based Pattern Matching**
   - Ekstraksi durasi dengan context-aware (mencegah "28 tahun" terdeteksi sebagai durasi)
   - Ekstraksi umur, nama, dan informasi terstruktur
   - Pattern validation untuk menghindari false positive

2. **Dictionary-based Keyword Matching**
   - Matching gejala dari `symptoms_dict.json` (50+ gejala dengan sinonim)
   - Identifikasi lokasi tubuh dari `location_keywords.json`
   - Klasifikasi severity dari `severity_keywords.json`

3. **Context-aware Extraction**
   - Membedakan "28 tahun" (umur) vs "3 hari" (durasi) berdasarkan kata konteks
   - Validasi dengan kata kunci seperti "sudah", "sejak", "selama" untuk durasi

**Contoh Implementasi:**
```python
class EntityExtractor:
    def extract_durasi(self, text):
        # Pattern dengan context untuk mencegah false positive
        duration_contexts = ['sudah', 'sejak', 'selama']
        for context in duration_contexts:
            pattern = rf'{context}\s+(\d+)\s*(?:hari|minggu|bulan)'
            match = re.search(pattern, text.lower())
            if match:
                return match.group(0)
        return None
```

**Entitas yang Diekstrak:**
- Nama lengkap dan nama panggilan
- Umur (dalam tahun)
- Jenis kelamin (laki-laki/perempuan)
- Gejala medis (dari dictionary 50+ gejala)
- Lokasi keluhan (20+ bagian tubuh)
- Durasi keluhan (hari, minggu, bulan, tahun)
- Tingkat keparahan (ringan, sedang, berat)

## Kontribusi

Untuk berkontribusi:

1. Fork repository ini
2. Buat branch baru: `git checkout -b feature-name`
3. Commit perubahan: `git commit -m 'Add feature'`
4. Push ke branch: `git push origin feature-name`
5. Buat Pull Request

## Troubleshooting

### Backend tidak bisa diakses
- Pastikan Flask server berjalan di port 5000
- Cek apakah model sudah di-load dengan mengakses `http://localhost:5000/health`

### Frontend tidak connect ke backend
- Periksa environment variable `NEXT_PUBLIC_API_URL`
- Pastikan tidak ada CORS error di browser console
- Cek apakah backend sudah berjalan

### Error saat training model
- Pastikan semua dependencies terinstall
- Cek apakah dataset ada di folder `data/`
- Pastikan virtual environment sudah diaktifkan

## Kontak

Untuk pertanyaan atau diskusi, silakan buat issue di repository ini.

