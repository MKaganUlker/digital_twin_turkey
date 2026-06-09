from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class TurkeyState:
    year: int

    # Core macro indicators
    gdp: float             # Milyar TL (nominal)
    inflation: float       # Yıllık % (ör: 65.0 = %65)
    interest_rate: float   # TCMB politika faizi %
    unemployment: float    # İşsizlik oranı %

    # Döviz
    currency_usd_try: float  # 1 USD = ? TRY

    # Harcama tarafı
    consumption: float     # Milyar TL
    investment: float      # Milyar TL

    def to_dict(self) -> dict:
        return asdict(self)


# Gerçek veriye dayalı başlangıç noktası (2023 yıl sonu yaklaşık değerler)
INITIAL_STATE = TurkeyState(
    year=2023,
    gdp=22_000.0,
    inflation=64.8,
    interest_rate=42.5,
    unemployment=8.7,
    currency_usd_try=29.5,
    consumption=14_000.0,
    investment=5_500.0,
)
