"""
TCMB (Türkiye Cumhuriyet Merkez Bankası) Veri Çekici

TCMB EVDS API'si üzerinden faiz, kur ve para arzı verilerini çeker.

API Belgesi: https://evds2.tcmb.gov.tr/help/videos/EVDS_Web_Service_Usage_Guide.pdf
API anahtarı için: https://evds2.tcmb.gov.tr/index.php?/evds/userDeal/
"""
import os
import requests
from datetime import datetime, date
from typing import Optional

EVDS_BASE = "https://evds2.tcmb.gov.tr/service/evds"

# Seri kodları
SERIES = {
    "policy_rate":    "TP.DK.USD.A.YTL",    # TCMB faiz kararı
    "usd_try":        "TP.DK.USD.A",         # USD/TRY kur
    "money_supply_m2": "TP.PA.M2",           # M2 para arzı
}


def fetch_series(
    series_key: str,
    start_date: str = "01-01-2020",
    end_date: Optional[str] = None,
    api_key: Optional[str] = None,
) -> list:
    """
    TCMB EVDS'den bir veri serisi çek.
    
    api_key: EVDS API anahtarı. Yoksa env'den TCMB_API_KEY okunur.
    Döndürür: [{"date": "...", "value": ...}, ...]
    """
    key = api_key or os.getenv("TCMB_API_KEY")
    if not key:
        print("[TCMB] API anahtarı yok — mock veri dönüyor")
        return _mock_data(series_key)

    end = end_date or datetime.today().strftime("%d-%m-%Y")
    series_code = SERIES.get(series_key, series_key)

    url = (
        f"{EVDS_BASE}/series={series_code}"
        f"&startDate={start_date}&endDate={end}"
        f"&type=json&key={key}"
    )

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return [
            {"date": item.get("Tarih"), "value": float(item.get(series_code, 0) or 0)}
            for item in items
            if item.get(series_code) not in (None, "")
        ]
    except Exception as e:
        print(f"[TCMB] Fetch hatası: {e} — mock data kullanılıyor")
        return _mock_data(series_key)


def _mock_data(series_key: str) -> list:
    """API anahtarı olmadan test için mock data."""
    mock = {
        "policy_rate": [
            {"date": "2023-01", "value": 9.0},
            {"date": "2023-06", "value": 15.0},
            {"date": "2023-12", "value": 42.5},
        ],
        "usd_try": [
            {"date": "2023-01", "value": 18.8},
            {"date": "2023-06", "value": 23.5},
            {"date": "2023-12", "value": 29.5},
        ],
    }
    return mock.get(series_key, [])


if __name__ == "__main__":
    print("Faiz verisi (mock):")
    for row in fetch_series("policy_rate"):
        print(f"  {row['date']}: %{row['value']}")
    print("\nDolar kuru (mock):")
    for row in fetch_series("usd_try"):
        print(f"  {row['date']}: {row['value']} TL")
