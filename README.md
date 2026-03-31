# 🚀 MemeSearch: Cross-Modal Meme Retrieval Engine
Penerapan Sistem Temu Kembali menggunakan model CLIP untuk mencari gambar meme dengan kata kata descriptif
Proyek ini adalah mesin pencari meme berbasis kecerdasan buatan (*Artificial Intelligence*) yang menggunakan model **Multilingual CLIP**, database vektor **FAISS**, dan **MongoDB** untuk metadata. Pengguna dapat mencari gambar meme hanya dengan mendeskripsikan konteks visual atau teks yang ada di dalam meme menggunakan Bahasa Indonesia.

## 📋 Prasyarat Sistem
Sebelum menjalankan aplikasi, pastikan sistem kamu sudah terinstal:
* **Python 3.8+**
* **Node.js & npm** (Untuk menjalankan Frontend React)
* **MongoDB** (Berjalan secara lokal di `mongodb://localhost:27017` atau menggunakan MongoDB Atlas)

---

## 🛠️ Cara Instalasi & Menjalankan Aplikasi

Langkah-langkah di bawah ini harus dijalankan setelah kamu berhasil melakukan *clone* repositori ini.

### 1. Setup Backend (Python & AI)
Buka terminal dan arahkan ke dalam folder `backend` proyek ini.

```bash
cd backend

# Untuk Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# Untuk Mac/Linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Proses Indexing Data (Wajib Dilakukan Pertama Kali)
# Masukkan gambar-gambar meme (format .jpg, .png, .webp) ke dalam folder backend/data/images/.
# Jalankan skrip indexer untuk mengekstrak vektor dan membaca teks (OCR) pada meme
python indexer.py

# nyalakan server
uvicorn main:app --reload

# nyalakan frontend
cd frontend
npm install
npm run dev
```








