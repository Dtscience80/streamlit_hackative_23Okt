# EduML — Chatbot Edukasi Machine Learning

EduML adalah aplikasi chatbot edukasi berbasis Streamlit dan Google Gemini API untuk membantu siswa SMA/SMK (STM) mengenal konsep Machine Learning dengan bahasa yang ramah dan bertahap.

## Fitur

- UI profesional, ceria, dan futuristik dengan gradasi ungu-biru-pink, aksen cyan, kartu modern, serta panel pengaturan yang responsif.
- API key Google Gemini dimasukkan manual melalui sidebar.
- Pilihan model Gemini.
- Parameter LLM: temperature, top-p, dan batas token keluaran.
- Pengaturan gaya mengajar, tingkat materi, dan instruksi tambahan.
- Prompt cepat untuk topik dasar, AI vs ML, jenis ML, proyek sekolah, Python, dan kuis.
- Riwayat chat selama sesi Streamlit aktif dan tombol reset.
- System instruction dirancang untuk pelajar tingkat sekolah menengah serta menekankan etika dan keterbatasan AI.

## Struktur repository

```text
.
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Persyaratan

- Python 3.10 atau lebih baru.
- Google Gemini API key dari [Google AI Studio](https://aistudio.google.com/apikey).
- Koneksi internet saat menjalankan aplikasi.

## Jalankan di komputer lokal

Buat dan aktifkan virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependensi dan jalankan:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Buka URL lokal yang ditampilkan Streamlit, biasanya `http://localhost:8501`. Masukkan API key pada sidebar.

## Deploy ke GitHub dan Streamlit Community Cloud

1. Buat repository di [GitHub](https://github.com/new).
2. Unggah `app.py`, `requirements.txt`, `README.md`, dan `.gitignore` ke root repository.
3. Jangan commit API key atau kredensial.
4. Buka [Streamlit Community Cloud](https://share.streamlit.io/) dan login dengan GitHub.
5. Pilih **Create app**, lalu pilih repository, branch `main`, dan file utama `app.py`.
6. Klik **Deploy**. Karena API key dimasukkan manual di sidebar, Anda tidak perlu menaruh key di source code atau Secrets untuk pola penggunaan ini.

## Parameter model

- **Temperature (0.0–1.5):** nilai rendah cenderung menghasilkan jawaban lebih konsisten; nilai tinggi lebih bervariasi. Nilai awal 0.5 dipilih untuk pembelajaran.
- **Top-p (0.1–1.0):** mengatur cakupan kandidat token yang dipertimbangkan saat menghasilkan teks. Nilai awal 0.9.
- **Maximum output tokens:** membatasi panjang keluaran model. Nilai awal 1536 token.
- **Model:** daftar model disediakan di aplikasi. Model yang benar-benar tersedia dapat bergantung pada akses dan kebijakan akun Google.

Perubahan konfigurasi memulai konteks percakapan baru agar pengaturan yang terlihat konsisten dengan sesi model yang aktif.

## Keamanan dan keterbatasan

- API key dimasukkan sebagai input bertipe password dan tidak ditulis ke file Python. Hindari membagikan layar atau perangkat ketika key sedang dimasukkan.
- Jangan pernah menambahkan API key ke GitHub.
- Riwayat percakapan tersimpan di session state dan bukan penyimpanan permanen.
- Respons AI bisa keliru. Verifikasi informasi penting, khususnya ketika mengerjakan tugas sekolah atau membuat proyek.
- Penggunaan API dapat tunduk pada kuota, biaya, serta ketentuan Google yang berlaku.

## Troubleshooting

- **API key ditolak:** pastikan key benar, aktif, dan memiliki akses ke Gemini API.
- **Model tidak tersedia:** pilih model lain dari dropdown atau periksa model yang didukung akun Anda.
- **Quota / rate limit:** periksa kuota dan penggunaan pada Google AI Studio.
- **Dependency error:** gunakan Python 3.10+ lalu jalankan ulang `pip install -r requirements.txt`.
