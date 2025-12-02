export interface ChatMessage {
  id: string;
  role: 'user' | 'bot';
  content: string;
  intent?: string;
  confidence?: number;
  timestamp: Date;
}

export interface SessionResponse {
  session_id: string;
  bot_message: string;
  state: string;
}

export interface ChatResponse {
  session_id: string;
  intent: string;
  confidence: number;
  bot_message: string;
  state: string;
  entities?: {
    nama?: string;
    umur?: string;
    jenis_kelamin?: string;
    durasi?: string;
    lokasi?: string;
    severity?: string;
    symptoms?: string[];
  };
}

export interface AnamnesisSummary {
  identitas: {
    nama: string;
    usia: string;
    jenis_kelamin: string;
  };
  anamnesis: {
    keluhan_utama: string;
    gejala_penyerta?: string;
    durasi?: string;
    lokasi?: string;
    tingkat_keparahan?: string;
  };
  riwayat: {
    riwayat_penyakit?: string;
    obat_dikonsumsi?: string;
    riwayat_alergi?: string;
    faktor_risiko?: string;
  };
}
