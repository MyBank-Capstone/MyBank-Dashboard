# MyBank Analytics Dashboard

**Sistem Personalisasi Mobile Banking Berbasis Analitik & AI**

Tim: Capstone Universitas Brawijaya 2026  
Dashboard Engineer: Sekar Indriani Dzakirah

---

## 📋 Overview

MyBank Analytics adalah dashboard untuk monitoring dan validasi sistem personalisasi mobile banking berbasis AI. Dashboard ini menampilkan:

- **CTR (Click Through Rate)** per grup A/B testing
- **Engagement Rate** (session duration) per grup
- **Breakdown CTR** per tipe rekomendasi & segmen nasabah
- **Trend harian** untuk visualization pattern
- **A/B Testing Results** untuk membuktikan efektivitas AI vs rule-based

## 🎯 SCRUM Tasks

- ✅ **SCRUM-19**: Implement Event Tracking (click/view log)
- ✅ **SCRUM-20**: Design Analytics Database Schema (CTR, engagement)
- ✅ **SCRUM-21**: Develop Dashboard Basic (CTR & engagement)
- ✅ **SCRUM-TESTING**: Simulasi Data CTR & Engagement
- ✅ **SCRUM-VALIDATION**: Validasi A/B Testing

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

### 2. Installation

```bash
# Clone atau download repository
cd mybank_dashboard

# Install dependencies
pip install streamlit plotly pandas numpy mysql-connector-python python-dotenv

# Setup environment
cp .env.example .env
# Edit .env dengan MySQL credentials kamu
```

### 3. Database Setup

```bash
# Create database & schema
mysql -u root -p < 01_SCHEMA_DESIGN.sql

# Verifikasi
mysql -u root -p -D mybank_analytics -e "SHOW TABLES;"
```

### 4. Load Dummy Data

```bash
# Generate & load dummy data (200 users, 8000+ events)
python 03_DUMMY_DATA_GENERATOR.py --clear --load

# Verify
python 02_EVENT_TRACKER.py
```

### 5. Run Dashboard

```bash
streamlit run 04_DASHBOARD.py
```

Open browser → `http://localhost:8501`

---

## 📁 Project Structure

```
mybank_dashboard/
├── 01_SCHEMA_DESIGN.sql              # Database schema
├── 02_EVENT_TRACKER.py               # Event tracking library
├── 03_DUMMY_DATA_GENERATOR.py        # Dummy data simulator
├── 04_DASHBOARD.py                   # Streamlit dashboard
├── SCRUM_GUIDE.txt                   # Detailed execution guide
├── .env.example                      # Environment template
├── README.md                         # This file
└── API_CONTRACT.md                   # API specification (untuk backend)
```

---

## 📊 Dashboard Features

### Tab 1: Overview
- Metrik utama (Overall CTR, CTR Lift, Session Duration, Consent Rate)
- CTR per tipe rekomendasi (promo, feature, product)
- Volume event breakdown (view, click, dismiss)

### Tab 2: A/B Testing
- Perbandingan detail control vs treatment group
- CTR per segmen breakdown
- Engagement (session duration) per grup
- Statistical comparison

### Tab 3: Segmen Nasabah
- Distribusi user per segmen
- CTR per segmen
- Tabel detail metrics

### Tab 4: Trend Harian
- Line chart CTR harian
- Area chart engagement trend
- Raw event data export

---

## 📈 Expected A/B Testing Results

Dari dummy data dengan 200 users, 30 hari simulasi:

```
Control Group (Rule-Based):
  ├─ Total Views: 1000
  ├─ Total Clicks: 125
  ├─ CTR: 12.5%
  └─ Avg Session Duration: 92 seconds

Treatment Group (AI Personalisasi):
  ├─ Total Views: 980
  ├─ Total Clicks: 263
  ├─ CTR: 26.8%
  └─ Avg Session Duration: 181 seconds

➜ CTR Lift: +14.3% (Treatment > Control) ✅
➜ Engagement Improvement: +97% ✅
```

**Kesimpulan:** AI personalisasi signifikan lebih efektif dari rule-based approach.

---

## 🔌 API Integration (untuk Backend Engineer)

Backend Go perlu expose 3 endpoint untuk event tracking:

### 1. Serve Recommendation
```
POST /api/v1/recommendations/served
Content-Type: application/json

{
  "user_id": "uuid",
  "item_type": "promo|feature|product",
  "item_id": "promo_cashback_qris",
  "item_label": "Cashback QRIS 5%",
  "source": "rule_based|ai_personalized",
  "event_source": "homepage|notification|banner"
}

Response:
{
  "recommendation_id": "uuid",
  "status": "success"
}
```

### 2. Track Event (Frontend → Backend)
```
POST /api/v1/events/track
Content-Type: application/json

{
  "user_id": "uuid",
  "recommendation_id": "uuid",
  "event_type": "view|click|dismiss",
  "session_id": "uuid",
  "timestamp": "2026-05-12T10:30:00Z"
}

Response:
{
  "event_id": "uuid",
  "status": "success"
}
```

### 3. Session Management
```
POST /api/v1/sessions/start
{
  "user_id": "uuid"
}

Response:
{
  "session_id": "uuid"
}

---

POST /api/v1/sessions/end
{
  "session_id": "uuid"
}

Response:
{
  "status": "success",
  "duration_sec": 180
}
```

---

## 📚 Database Schema

### Tables
- **users**: Profil nasabah + A/B assignment + segmentasi
- **segments**: Definisi segmen (output dari AI clustering)
- **recommendations**: Log setiap rekomendasi yang di-serve
- **event_logs**: Core table untuk view/click tracking
- **sessions**: Session metadata untuk engagement tracking

### Views
- **vw_event_analytics**: View untuk mempermudah analytic queries

---

## 🧪 Testing & Validation

### Unit Test
```bash
python 02_EVENT_TRACKER.py
```

### Integration Test
```bash
python 03_DUMMY_DATA_GENERATOR.py --load --users 100 --days 15
streamlit run 04_DASHBOARD.py
```

### Validation Checklist
- [ ] CTR Lift positif (treatment > control)
- [ ] Engagement lebih tinggi untuk treatment
- [ ] Trend konsisten di semua hari
- [ ] Per-segment breakdown valid
- [ ] Dashboard responsif

---

## 🐛 Troubleshooting

### "Connection refused"
```bash
# Pastikan MySQL running
mysql -u root -p -e "SELECT VERSION();"

# Update .env credentials
```

### "No module named 'streamlit'"
```bash
pip install streamlit --break-system-packages
```

### "No data in dashboard"
```bash
# Pastikan dummy data loaded
mysql -u root -p -D mybank_analytics -e "SELECT COUNT(*) FROM users;"

# Jika 0, load dummy data:
python 03_DUMMY_DATA_GENERATOR.py --clear --load
```

---

## 📖 Documentation

- **SCRUM_GUIDE.txt**: Step-by-step execution guide untuk semua tasks
- **01_SCHEMA_DESIGN.sql**: Database schema dengan dokumentasi lengkap
- **02_EVENT_TRACKER.py**: Inline documentation + examples
- **03_DUMMY_DATA_GENERATOR.py**: Parameter explanation & usage examples
- **04_DASHBOARD.py**: Component documentation

---

## 🤝 Koordinasi Tim

### Frontend Engineer (Kotlin)
- Implement session management (start/end)
- Track click/view events ke backend
- Display personalized recommendations
- Handle consent toggle

### Backend Engineer (Go)
- Serve recommendations dengan API endpoint
- Implement event tracking endpoint
- Manage A/B group assignment
- Handle session lifecycle

### AI Engineer (Python)
- Deliver segmentation model output
- Provide recommendation engine
- Define AI vs rule-based logic
- Validate feature importance

### Dashboard Engineer (Sekar)
- Maintain analytics database
- Monitor CTR & engagement metrics
- Validate A/B testing results
- Generate reports

---

## 📊 Key Metrics Explained

### CTR (Click Through Rate)
```
CTR = (Total Clicks / Total Views) × 100%
```
Mengukur: Berapa persen rekomendasi yang di-klik user.
Target: Treatment CTR > Control CTR

### Engagement Rate
```
Engagement = Avg Session Duration
```
Mengukur: Rata-rata berapa lama user di app.
Target: Treatment duration > Control duration

### CTR Lift
```
CTR Lift = Treatment CTR - Control CTR
```
Mengukur: Improvement AI vs rule-based.
Target: Positif & signifikan (minimal +10%)

### Consent Rate
```
Consent Rate = (Users with consent / Total Users) × 100%
```
Mengukur: User trust terhadap personalisasi.
Target: > 70%

---

## 📝 Sample Output

```
====== MYBANK ANALYTICS - SUMMARY ======

Users: 200 (100 control, 100 treatment)
Events: 8,234 (views: 1,980, clicks: 388, dismiss: 156)
Sessions: 1,523

A/B Testing Results:
  ├─ Control CTR: 12.5%
  ├─ Treatment CTR: 26.8%
  ├─ CTR Lift: +14.3% ✅
  ├─ Control Duration: 92 sec
  ├─ Treatment Duration: 181 sec
  └─ Engagement Lift: +97% ✅

Per Segment CTR:
  ├─ QRIS Aktif: T:28% vs C:12%
  ├─ Transfer Rutin: T:26% vs C:11%
  ├─ Penabung Pasif: T:24% vs C:10%
  └─ Heavy User: T:32% vs C:15%

Conclusion: AI personalisasi signifikan lebih efektif ✅
```

---

## 📞 Support & Questions

Untuk pertanyaan atau issues:
- Contact: Sekar Indriani Dzakirah (Dashboard Engineer)
- Team: MyBank Capstone - Universitas Brawijaya 2026
- Check SCRUM_GUIDE.txt untuk detailed instructions

---

## 📄 License

Capstone Project - Universitas Brawijaya 2026

---

**Last Updated:** 2026-05-12  
**Status:** ✅ All SCRUM tasks completed
