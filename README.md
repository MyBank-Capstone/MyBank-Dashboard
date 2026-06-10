# MyBank Analytics Dashboard

MyBank Analytics Dashboard merupakan aplikasi visualisasi data berbasis Streamlit yang dikembangkan untuk mendukung proses analisis performa sistem rekomendasi pada aplikasi MyBank. Dashboard ini digunakan untuk memantau efektivitas rekomendasi berdasarkan interaksi pengguna melalui metrik seperti Click Through Rate (CTR), engagement rate, segmentasi pengguna, dan hasil simulasi A/B testing.

Dashboard menggunakan data dummy dalam format Excel sebagai sumber data utama. Data tersebut diproses secara langsung untuk menghasilkan insight mengenai perilaku pengguna tanpa membutuhkan koneksi database tambahan.

## Features

Beberapa fitur utama yang tersedia pada dashboard:

- Monitoring performa rekomendasi berdasarkan CTR
- Perbandingan performa rekomendasi antara control group dan treatment group
- Analisis engagement pengguna berdasarkan durasi sesi
- Visualisasi distribusi segmen pengguna
- Analisis tren interaksi pengguna berdasarkan waktu
- Tampilan raw data untuk kebutuhan monitoring dan validasi

## Tech Stack

Project ini dikembangkan menggunakan:

- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL

## Project Structure

```

MyBank-Dashboard/

├── dashboard.py
├── MyBank Data.xlsx
├── requirements.txt
└── README.md

```

Keterangan:

- `dashboard.py`  
  File utama aplikasi Streamlit yang berisi proses load data, transformasi data, perhitungan metrik, dan visualisasi dashboard.

- `MyBank Data.xlsx`  
  Dataset dummy yang digunakan sebagai sumber data analytics.

- `requirements.txt`  
  Berisi daftar library Python yang diperlukan untuk menjalankan aplikasi.

## Dataset

Dataset dummy terdiri dari beberapa data utama:

### Accounts

Berisi informasi pengguna seperti:

- Nomor rekening
- Profil pengguna
- Pekerjaan
- Pendapatan
- Jenis akun
- Informasi akun

### Transactions

Berisi data transaksi pengguna seperti:

- ID transaksi
- Nomor rekening
- Tanggal transaksi
- Nominal transaksi
- Kategori transaksi
- Merchant
- Channel transaksi

### Merchants

Berisi informasi merchant yang digunakan pada transaksi.

### User Interactions

Berisi simulasi aktivitas pengguna yang digunakan untuk analisis perilaku pengguna.

## Analytics Metrics

### Click Through Rate (CTR)

CTR digunakan untuk mengukur persentase rekomendasi yang mendapatkan interaksi klik dari pengguna.

Perhitungan:

```

CTR = (Total Click / Total View) x 100%

````

### A/B Testing

Dashboard melakukan simulasi perbandingan antara:

- Control Group  
  Pengguna dengan rekomendasi berbasis rule-based.

- Treatment Group  
  Pengguna dengan rekomendasi berbasis personalisasi AI.

Hasil perbandingan digunakan untuk melihat peningkatan performa rekomendasi berdasarkan CTR dan engagement pengguna.

### Engagement Rate

Engagement dianalisis berdasarkan rata-rata durasi sesi pengguna untuk melihat tingkat keterlibatan pengguna terhadap aplikasi.

## Installation

Clone repository:

```bash
git clone https://github.com/MyBank-Capstone/MyBank-Dashboard.git
````

Masuk ke folder project:

```bash
cd MyBank-Dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Jalankan aplikasi:

```bash
streamlit run dashboard.py
```

## Deployment

Dashboard telah dideploy menggunakan Streamlit Community Cloud.

Link dashboard:

```
https://mybank-dashboard.streamlit.app/
```

## Role

Dashboard Engineer

Kontribusi:

* Mendesain kebutuhan analitik dashboard
* Melakukan transformasi data dummy
* Mengembangkan visualisasi metrik rekomendasi
* Mengimplementasikan analisis CTR dan engagement
* Melakukan deployment dashboard berbasis Streamlit Cloud

## MyBank Capstone Project

Dashboard ini merupakan bagian dari pengembangan sistem MyBank yang berfokus pada analisis performa rekomendasi dan personalisasi pengguna.
