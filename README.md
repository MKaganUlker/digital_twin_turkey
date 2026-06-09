<div align="center">

![Digital Twin Türkiye](assets/banner.svg)

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          DIGITAL TWIN TÜRKİYE  ·  v0.1                      ║
║          Makroekonomik Simülasyon Motoru                     ║
║                                                              ║
║          GDP  ·  Enflasyon  ·  Faiz  ·  İşsizlik            ║
║          Döviz  ·  Tüketim  ·  Yatırım                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-E85D24?style=flat-square)](LICENSE)

</div>

---

## Ne Yapar?

Türkiye ekonomisini adım adım simüle eder. Faiz artırdığında enflasyon nasıl düşer? Döviz kuru nereye gider? İşsizlik ne olur? Bunları **gerçek başlangıç verisiyle** (TCMB + TÜİK) modelleyip görürsün.

```
politika faizi ↑  →  kredi maliyeti ↑  →  talep ↓  →  enflasyon ↓
enflasyon ↑       →  satın alma gücü ↓ →  tüketim ↓
enflasyon ↑       →  TL değer kaybı ↑  →  kur ↑
```

---

## Canlı Çıktı — Baz Senaryo (Faiz %42.5, 2023 Başlangıcı)

```
$ curl "localhost:8000/simulate?years=6"

YIL  │  GDP (Milyar ₺)       │  Enflasyon  │  USD/TRY  │  İşsizlik
─────┼───────────────────────┼─────────────┼───────────┼──────────
2024 │  21,117  ▓▓▓▓▓▓▓▓▓▓  │    48.0%    │    38.78  │    9.0%
2025 │  19,055  ▓▓▓▓▓▓▓▓▓   │    35.5%    │    34.00  │    9.2%
2026 │  17,687  ▓▓▓▓▓▓▓▓    │    26.3%    │    11.92  │    9.3%
2027 │  16,760  ▓▓▓▓▓▓▓▓    │    19.4%    │     8.40  │    9.3%
2028 │  16,133  ▓▓▓▓▓▓▓▓    │    14.4%    │     6.10  │    9.2%
2029 │  15,722  ▓▓▓▓▓▓▓     │    10.6%    │     4.80  │    9.1%
```

**Senaryo karşılaştırması** — Enflasyonun düşüş hızı faize göre nasıl değişir:

```
           Faiz %42.5 (baz)       Faiz %60 (sıkı)
           ───────────────        ───────────────
2024       48.0%  █████████       38.9%  ███████
2025       35.5%  ███████         23.3%  ████
2026       26.3%  █████           14.0%  ██
2027       19.4%  ███              8.4%  █
2028       14.4%  ██               5.0%  █
```

---

## Başlangıç

```bash
# 1. Klonla
git clone https://github.com/kullanicin/digital-twin-turkey
cd digital-twin-turkey

# 2. Bağımlılıkları kur
cd backend && pip install -r requirements.txt

# 3. Çalıştır
uvicorn app.main:app --reload --port 8000

# 4. Test et
curl "localhost:8000/simulate?years=10"
curl "localhost:8000/simulate/scenarios"
curl "localhost:8000/real-data/latest"
```

---

## API Referansı

| Endpoint | Parametre | Açıklama |
|---|---|---|
| `GET /simulate` | `years`, `interest_override`, `inflation_override` | Simülasyon çalıştır |
| `GET /simulate/shock` | `shock_year`, `shock_inflation`, `shock_interest` | Dışsal şok ekle |
| `GET /simulate/scenarios` | — | Baz / sıkı / gevşek 3 senaryo |
| `GET /real-data/latest` | — | TCMB + TÜİK snapshot |

### Örnek: Faizi değiştirerek simüle et

```bash
# Faiz %25 olsa ne olurdu?
curl "localhost:8000/simulate?years=10&interest_override=25"

# Yıl 3'te enflasyon şoku
curl "localhost:8000/simulate/shock?shock_year=3&shock_inflation=30&years=10"
```

---

## Simülasyon Motoru

Her `step()` çağrısı bir yılı geçirir. Sıra önemlidir:

```python
def step(state: TurkeyState) -> TurkeyState:

    # 1. Faiz → Enflasyon  (para politikası etkisi)
    rate_effect  = (state.interest_rate - 10) * INTEREST_TO_INFLATION
    state.inflation *= (1 - rate_effect)

    # 2. Enflasyon → Tüketim  (satın alma gücü kaybı)
    state.consumption *= (TREND_GROWTH - state.inflation * INFLATION_TO_CONSUMPTION)

    # 3. Faiz → Yatırım  (kredi maliyeti etkisi)
    state.investment  *= (TREND_GROWTH - state.interest_rate * INTEREST_TO_INVESTMENT)

    # 4. GDP kimliği  (harcama yaklaşımı)
    state.gdp = (state.consumption + state.investment) * 1.25

    # 5. Enflasyon → İşsizlik  (ters Phillips eğrisi)
    state.unemployment += (state.inflation - 20) * INFLATION_TO_UNEMPLOYMENT

    # 6. Enflasyon → Döviz  (satın alma gücü paritesi)
    state.currency_usd_try *= (1 + effective_inflation * PASS_THROUGH)

    return state
```

Tüm katsayılar [`simulation/parameters.py`](backend/app/simulation/parameters.py) içinde — modeli buradan kalibre edebilirsin.

---

## Proje Yapısı

```
digital_twin_turkey/
│
├── backend/
│   ├── app/
│   │   ├── main.py                        ← app factory (create_app)
│   │   ├── core/
│   │   │   ├── config.py                  ← tüm ayarlar tek yerden (Settings)
│   │   │   ├── exceptions.py              ← typed hata sınıfları
│   │   │   └── logging.py                 ← merkezi loglama
│   │   ├── api/v1/
│   │   │   └── router.py                  ← ince HTTP katmanı, sadece routing
│   │   ├── models/
│   │   │   ├── state.py                   ← TurkeyState domain modeli
│   │   │   └── schemas.py                 ← Pydantic request/response şemaları
│   │   ├── services/
│   │   │   ├── simulation_service.py      ← simülasyon iş mantığı
│   │   │   └── data_service.py            ← veri kaynağı soyutlaması
│   │   ├── simulation/
│   │   │   ├── macro_model.py             ← step() · run_simulation()
│   │   │   └── parameters.py              ← kalibre edilebilir katsayılar
│   │   └── repositories/
│   │       ├── tcmb_repository.py         ← TCMB EVDS erişimi
│   │       └── simulation_repository.py   ← PostgreSQL (v0.2)
│   ├── tests/
│   │   ├── unit/test_simulation.py        ← simülasyon motor testleri
│   │   └── integration/                   ← API entegrasyon testleri (v0.2)
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── pages/                         ← Next.js sayfa bileşenleri
│       ├── components/                    ← paylaşılan UI bileşenleri
│       ├── charts/                        ← Recharts grafik bileşenleri
│       ├── services/                      ← API istemcisi
│       └── hooks/                         ← custom React hook'ları
│
├── database/
│   └── migrations/
│       └── 001_initial_schema.sql         ← versiyonlu migration'lar
│
├── infra/
│   ├── docker/
│   │   └── backend.Dockerfile
│   └── nginx/                             ← reverse proxy (v0.2)
│
├── docker-compose.yml                     ← tek komutla tüm stack
├── Makefile                               ← make dev · make test · make docker-up
└── .gitignore
```

**Katman sorumluluğu:**

| Katman | Nerede | Ne yapar |
|---|---|---|
| HTTP | `api/v1/router.py` | Sadece routing ve validation |
| Business logic | `services/` | İş kuralları, use-case'ler |
| Domain | `models/state.py` | Saf veri yapıları |
| Schemas | `models/schemas.py` | API giriş/çıkış kontratları |
| Simulation | `simulation/` | Matematiksel model |
| Data access | `repositories/` | Dış dünya (DB, API) |
| Config | `core/config.py` | Tüm ayarlar tek yerden |

---

## Veri Kaynakları

| Gösterge | Kaynak | Seri |
|---|---|---|
| Politika faizi | TCMB EVDS | `TP.DK.USD.A.YTL` |
| USD/TRY kuru | TCMB EVDS | `TP.DK.USD.A` |
| Enflasyon (TÜFE) | TÜİK | yıllık % değişim |
| İşsizlik | TÜİK | mevsim düzeltilmiş |
| GDP | TÜİK | nominal, milyar ₺ |

TCMB API anahtarı almak için: [evds2.tcmb.gov.tr](https://evds2.tcmb.gov.tr/index.php?/evds/userDeal/)  
`.env` dosyasına `TCMB_API_KEY=...` olarak ekle.

---

## Yol Haritası

```
v0.1  ✓  Simülasyon motoru · FastAPI · TCMB mock entegrasyonu
v0.2  ○  React dashboard · Recharts grafikleri · PostgreSQL
v0.3  ○  TCMB EVDS gerçek API · TÜİK scraper
v0.4  ○  Şehir bazlı ekonomi modeli (81 il)
v0.5  ○  Şirket ve hane halkı agent sistemi
v1.0  ○  AI karar katmanı · Monte Carlo şok simülasyonu
```

---

<div align="center">

`Python` · `FastAPI` · `PostgreSQL` · `Pandas` · `React` · `Recharts`

</div>