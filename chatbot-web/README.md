# Chatbot PUSTU - Web Application

Web application untuk chatbot anamnesis pasien Puskesmas Pembantu menggunakan NLP + Naive Bayes.

## Struktur

```
chatbot-web/
├── backend/          # Flask API server
└── frontend/         # Next.js 14 + TypeScript
```

## Quick Start

### Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Server berjalan di `http://localhost:5000`

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
Web app berjalan di `http://localhost:3000`

## Fitur

- Chat interface responsif (desktop & mobile)
- Dark/Light mode toggle
- Download hasil anamnesis ke PDF
- Real-time conversation dengan NLP backend
- Auto-scroll dan typing indicator

## Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS v4
- Axios
- jsPDF

**Backend:**
- Flask
- Scikit-learn (Naive Bayes)
- NLTK

## Deployment

- **Frontend**: Vercel
- **Backend**: Railway

Lihat file `.env.example` untuk konfigurasi environment variables.
