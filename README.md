# Digital Twin Türkiye v0.1

Türkiye makroekonomik simülasyon motoru.

## Hızlı Başlangıç

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoint'leri

| Endpoint | Açıklama |
|---|---|
| `GET /simulate?years=10` | 10 yıllık simülasyon |
| `GET /simulate?interest_override=30` | Faizi değiştirerek simüle et |
| `GET /simulate/shock?shock_year=3&shock_inflation=20` | Yıl 3'te enflasyon şoku |
| `GET /simulate/scenarios` | 3 senaryo karşılaştırması |
| `GET /real-data/latest` | TCMB + TÜİK son snapshot |

## Örnek İstek

```bash
curl "http://localhost:8000/simulate?years=5&interest_override=25"
```

```json
[
  {"year": 2023, "gdp": 22000.0, "inflation": 64.8, ...},
  {"year": 2024, "gdp": 24500.0, "inflation": 52.1, ...},
  ...
]
```

## Proje Yapısı

```
backend/
  app/
    main.py              ← FastAPI uygulaması
    models/state.py      ← TurkeyState veri modeli
    simulation/
      macro_model.py     ← step() ve run_simulation()
      parameters.py      ← Ayarlanabilir katsayılar

data_pipeline/
  tcmb_fetcher.py        ← TCMB EVDS API bağlantısı
  tuik_mock_loader.py    ← TÜİK verisi (mock → gerçek)

database/
  schema.sql             ← PostgreSQL tablo tanımları
```

## Simülasyon Mantığı

```
faiz ↑ → enflasyon ↓ (para politikası etkisi)
enflasyon ↑ → tüketim ↓ (satın alma gücü kaybı)
faiz ↑ → yatırım ↓ (kredi maliyeti)
GDP = (tüketim + yatırım) × 1.25
enflasyon ↑ → işsizlik ↑ (uzun dönem yapısal etki)
enflasyon ↑ → TL değer kaybı (satın alma gücü paritesi)
```

## Sonraki Adımlar (v0.2)

- [ ] TCMB EVDS API gerçek entegrasyon
- [ ] PostgreSQL bağlantısı
- [ ] React frontend dashboard
- [ ] Şehir bazlı ekonomi modeli
