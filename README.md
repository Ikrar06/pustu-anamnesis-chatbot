# Pustu Chatbot — Anamnesis NLP (Early development)

Status: Early development (Proof-of-concept)
--------------------------------------------
Proyek ini sedang berada pada tahap awal pengembangan. Beberapa komponen dasar (kamus, stopwords, dan konsep NER sederhana) telah dibuat untuk mendukung eksperimen awal, namun fitur end-to-end seperti pelatihan model produksi, evaluasi menyeluruh, dan pipeline deployment masih dalam rencana.

Deskripsi singkat
-----------------
Pustu Chatbot adalah proyek proof-of-concept untuk membantu proses anamnesis pasien di fasilitas primer seperti Puskesmas/Pustu menggunakan pendekatan NLP yang ringan dan dibuat dari awal (tidak menggunakan framework ML besar). Fokusnya: ekstraksi entitas dari teks (symptoms, lokasi, durasi, severity), klasifikasi intent sederhana, dan dialog follow-up dasar untuk mengumpulkan informasi anamnesis.


Panduan cepat (ringkas)
-----------------------
1. (Opsional) Buat virtual environment

	 - Windows (PowerShell):
		 ```powershell
		 python -m venv .venv
		Catatan akhir
		------------
		Proyek ini dirancang sebagai starting point yang mudah diperluas — tujuan utama saat ini adalah memperkuat kamus dan pipeline preprocessing, lalu melanjutkan ke model training, evaluasi, dan pengujian lebih luas.

		---

		Dokumentasi lebih lengkap, notebook, dan panduan pengembangan ada di `panduan_pustu_chatbot.md`.
--------------------------------

- Training & evaluasi: ada script dan notebook yang menggunakan modul inti; jurnal percobaan, model, dan visualisasi disimpan di folder `outputs/`.
- Demo interaktif: jalankan demo/nteraksi di notebook atau panggil modul `PustuChatbot` dari `pustu_chatbot.py`.

Struktur direktori 
---------------------------
- `data/dictionaries/` — kamus simptom, lokasi, severity, dan stopwords.
- `data/raw/` — data mentah (diabaikan dari versi final jika sensitif).
- `data/processed/` — dataset yang telah diproses dan siap dipakai (train/test).
- `outputs/` — gambar visualisasi, model, dan file hasil anamnesis.
- `pustu_chatbot_complete.ipynb` — notebook panduan lengkap.

Catatan dan kebijakan dependensi
-------------------------------
- Proyek ini menggunakan pustaka Python sederhana (NumPy dan Matplotlib secara opsional) dan menghindari paket ML/transformer besar (seperti `sklearn`, `spacy`, `tensorflow`, `torch`, `transformers`) sesuai panduan pengembangan.
- `requirements.txt` berisi dependensi minimum untuk menjalankan notebook dan skrip demo.

Kontribusi
----------
Terima kasih jika Anda ingin berkontribusi. Idealnya buka issue atau pull request kecil (feature, perbaikan kamus, perbaikan NER, atau unit test).

Lisensi
-------
Tambahkan lisensi yang sesuai untuk proyek Anda (misal: MIT, Apache, dsb.).

Kontak
------
Untuk pertanyaan atau diskusi, tambahkan issue di GitHub atau kontak melalui profil pemilik repositori.

---

Dokumentasi lebih lengkap, notebook, dan panduan pengembangan ada di `panduan_pustu_chatbot.md`.
