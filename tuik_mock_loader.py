"""
TÜİK Veri Yükleyici — v0.1 Mock Versiyonu

TÜİK'in kamuya açık API'si sınırlı olduğundan,
v0.1'de gerçek verilere dayalı mock data kullanıyoruz.
v0.2'de scraping veya resmi veri kaynağı entegrasyonu yapılacak.
"""
import pandas as pd
from typing import List, Dict


# Gerçek kaynaklara dayalı Türkiye yıllık makro verileri (2018-2023)
TUIK_HISTORICAL = [
    {"year": 2018, "gdp": 3_706.0,  "inflation": 20.3, "unemployment": 11.0, "consumption": 2_400.0, "investment": 890.0},
    {"year": 2019, "gdp": 4_319.0,  "inflation": 15.2, "unemployment": 13.7, "consumption": 2_800.0, "investment": 950.0},
    {"year": 2020, "gdp": 5_049.0,  "inflation": 14.6, "unemployment": 13.2, "consumption": 3_200.0, "investment": 1_050.0},
    {"year": 2021, "gdp": 7_249.0,  "inflation": 19.6, "unemployment": 12.0, "consumption": 4_600.0, "investment": 1_550.0},
    {"year": 2022, "gdp": 12_809.0, "inflation": 72.3, "unemployment": 10.2, "consumption": 8_200.0, "investment": 2_900.0},
    {"year": 2023, "gdp": 22_000.0, "inflation": 64.8, "unemployment": 8.7,  "consumption": 14_000.0, "investment": 5_500.0},
]


def load_historical() -> pd.DataFrame:
    """Tarihsel TÜİK verisini DataFrame olarak döndür."""
    return pd.DataFrame(TUIK_HISTORICAL)


def get_latest_snapshot() -> Dict:
    """En son yıla ait veri snapshot'ı."""
    return TUIK_HISTORICAL[-1]


def validate_data(df: pd.DataFrame) -> bool:
    """Veri kalite kontrolü."""
    required_cols = {"year", "gdp", "inflation", "unemployment", "consumption", "investment"}
    if not required_cols.issubset(df.columns):
        return False
    if df["gdp"].isna().any() or df["inflation"].isna().any():
        return False
    if (df["inflation"] < 0).any():
        return False
    return True


if __name__ == "__main__":
    df = load_historical()
    print("TÜİK Tarihsel Veri:")
    print(df.to_string(index=False))
    print(f"\nVeri geçerli: {validate_data(df)}")
