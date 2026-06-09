"""
Simülasyon parametreleri.
Bu dosyadaki katsayıları değiştirerek modeli kalibrate edebilirsin.
"""

# Faizin enflasyona etkisi
# Faiz 1 puan arttığında enflasyon ne kadar düşer?
INTEREST_TO_INFLATION = 0.008

# Enflasyonun tüketime etkisi
# Enflasyon 1 puan arttığında tüketim büyümesi ne kadar azalır?
INFLATION_TO_CONSUMPTION = 0.004

# Faizin yatırıma etkisi
# Faiz 1 puan arttığında yatırım büyümesi ne kadar azalır?
INTEREST_TO_INVESTMENT = 0.003

# Enflasyonun işsizliğe etkisi (basitleştirilmiş ters Phillips eğrisi)
INFLATION_TO_UNEMPLOYMENT = 0.012

# Döviz kuru büyüme hızı (TL değer kaybı modeli)
# Enflasyon farkına bağlı (Satın Alma Gücü Paritesi yaklaşımı)
CURRENCY_INFLATION_PASS_THROUGH = 0.7

# Türkiye uzun dönem büyüme trendi (faiz etkisi olmadan)
TREND_GROWTH = 1.04  # %4 potansiyel büyüme

# Minimum/maksimum sınırlar (gerçekçilik için)
MIN_INFLATION = 5.0
MAX_INFLATION = 200.0
MIN_UNEMPLOYMENT = 5.0
MAX_UNEMPLOYMENT = 30.0
