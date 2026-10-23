# Gemini Chatbot dengan Streamlit

Aplikasi chatbot sederhana berbasis **Streamlit** dan **Google Gemini API**, diadaptasi dari notebook training `23okt_streamlit_for_chatbot.py`.

## Fitur

- Antarmuka chat menggunakan `st.chat_message()` dan `st.chat_input()`.
- Riwayat percakapan tersimpan selama sesi aplikasi aktif.
- Pengaturan model Gemini dari sidebar.
- Instruksi sistem dapat disesuaikan.
- Tombol untuk mereset percakapan.
- API key dapat dimasukkan melalui sidebar atau disimpan di Streamlit Secrets.

## Struktur repository

```text
.
├── app.py
├── requirements.txt
└── README.md
```

## 1. Menyiapkan Google Gemini API Key

1. Buka [Google AI Studio](https://aistudio.google.com/).
2. Buat atau salin API key.
3. Jangan menaruh API key langsung di source code atau repository GitHub publik.

## 2. Menjalankan secara lokal

Pastikan Python 3.10 atau lebih baru telah terpasang. Di terminal, jalankan:

```bash
python -m venv .venv
```

Aktifkan virtual environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependency dan jalankan aplikasi:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Buka alamat lokal yang ditampilkan oleh Streamlit, biasanya `http://localhost:8501`. Masukkan API key di sidebar.

## 3. Deploy ke GitHub

1. Buat repository baru di [GitHub](https://github.com/).
2. Unggah `app.py`, `requirements.txt`, dan `README.md` ke root repository.
3. Pastikan API key tidak ikut diunggah.
4. Commit dan push perubahan.

Jika menggunakan Git dari terminal:

```bash
git init
git add app.py requirements.txt README.md
git commit -m "Add Streamlit Gemini chatbot"
git branch -M main
git remote add origin https://github.com/USERNAME/NAMA-REPOSITORY.git
git push -u origin main
```

Ganti `USERNAME` dan `NAMA-REPOSITORY` dengan informasi repository Anda.

## 4. Deploy ke Streamlit Community Cloud

1. Buka [Streamlit Community Cloud](https://share.streamlit.io/).
2. Login dan hubungkan akun GitHub.
3. Pilih **Create app**.
4. Pilih repository, branch `main`, dan file utama `app.py`.
5. Pada bagian **Advanced settings / Secrets**, tambahkan:

```toml
GOOGLE_API_KEY = "MASUKKAN_API_KEY_ANDA"
```

6. Deploy aplikasi. Setelah selesai, Streamlit akan memberikan URL publik.

Aplikasi juga menyediakan kolom API key di sidebar. Untuk aplikasi publik, lebih disarankan memakai **Secrets** daripada meminta setiap pengunjung memasukkan key milik mereka sendiri.

## Catatan

- Penggunaan Gemini tunduk pada kuota, ketersediaan model, dan ketentuan Google AI Studio.
- Jika muncul error, periksa API key, kuota, koneksi, dan apakah model yang dipilih tersedia untuk akun Anda.
- Riwayat chat disimpan dalam session state aplikasi dan tidak dirancang sebagai penyimpanan permanen.
- Jangan commit file `.env`, token, atau kredensial ke repository publik.
