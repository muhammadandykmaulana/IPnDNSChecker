# 🛡️ Cyber Threat Analyzer (Pemindai IP & Domain)

Proyek ini adalah tugas untuk mata kuliah **Pemrograman Back-End** di **Institut Teknologi Tangerang Selatan (ITTS)**. Melalui proyek ini, saya membangun sebuah aplikasi web sederhana menggunakan Flask untuk mengecek reputasi keamanan dari sebuah IP Address atau Domain dengan memanfaatkan data dari API publik.

---

## 🎯 Tujuan Proyek
Tujuan utama dari pembuatan aplikasi ini adalah:
1. **Penyelesaian Tugas:** Memenuhi rubrik penilaian mata kuliah Pemrograman Back-End yang mewajibkan integrasi API publik menggunakan framework Flask.
2. **Implementasi HTTP Request:** Memahami cara kerja pengambilan data secara dinamis dari pihak ketiga menggunakan library `requests` di Python.
3. **Data Rendering:** Mempraktikkan cara melakukan *looping* dan menampilkan struktur data JSON berjenjang ke dalam bentuk tabel serta kartu menggunakan HTML template bawaan Flask (Jinja2).

## 💡 Kegunaan Aplikasi
Aplikasi ini sangat praktis untuk mengecek apakah sebuah target (IP/Domain) aman untuk diakses. Fitur utamanya terbagi dua:
* **Pencarian IP Address (via AbuseIPDB):** Mengetahui apakah suatu alamat IP pernah dilaporkan melakukan aktivitas berbahaya seperti serangan DDoS, *spam*, atau penyebaran *malware*. Aplikasi akan menampilkan skor risiko dan tabel riwayat laporan secara detail.
* **Pencarian Nama Domain (via VirusTotal):** Mengecek status sebuah alamat *website* berdasarkan hasil pemindaian dari puluhan vendor antivirus global. Fitur ini sangat membantu untuk mendeteksi apakah sebuah *link* terindikasi sebagai web *phishing* atau tempat distribusi *malware*.

## 🛠️ Tech Stack
* **Back-End:** Python 3, Flask
* **API Integration:** Library `requests`
* **Front-End:** HTML5, CSS3 (Vanilla)
* **Data Sources:** [AbuseIPDB API](https://www.abuseipdb.com/) & [VirusTotal API v3](https://docs.virustotal.com/)

---

## 🚀 Cara Menjalankan Proyek

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di komputermu sendiri atau melalui GitHub Codespaces.

### 1. Persiapan API Key
Karena aplikasi ini menggunakan API publik, pastikan kamu sudah memiliki *key* aksesnya:
* Buat akun di [AbuseIPDB](https://www.abuseipdb.com/) lalu masuk ke halaman API untuk men-generate API Key.
* Buat akun di [VirusTotal](https://www.virustotal.com/), masuk ke menu profil, dan salin API Key.

### 2. Kloning Repositori & Install Library
Buka terminal dan jalankan perintah berikut:

```bash
# Clone repository ini
git clone [https://github.com/muhammadandykmaulana/IPnDNSChecker.git](https://github.com/muhammadandykmaulana/IPnDNSChecker.git)

# Masuk ke dalam folder proyek
cd IPnDNSChecker

# Install library yang dibutuhkan (Flask dan requests)
pip install Flask requests
```

### 3. Masukkan API Key ke dalam Kode
Buka file `app.py`. Cari baris kode di bawah ini dan tempelkan API Key yang sudah didapatkan pada langkah pertama:

```python
ABUSEIPDB_API_KEY = 'MASUKKAN_API_KEY_ABUSEIPDB_DISINI'
VIRUSTOTAL_API_KEY = 'MASUKKAN_API_KEY_VIRUSTOTAL_DISINI'
```

### 4. Jalankan Aplikasi
Masih di dalam terminal, jalankan server Flask dengan perintah:

`python app.py`