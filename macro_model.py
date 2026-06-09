"""
Digital Twin Türkiye — Makro Simülasyon Motoru v0.1

Deterministik, adım-bazlı ekonomi modeli.
Her step() çağrısı bir yılı simüle eder.
"""
import copy
from typing import List, Optional
from ..models.state import TurkeyState
from . import parameters as P


def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(max_val, value))


def step(state: TurkeyState, shock: Optional[dict] = None) -> TurkeyState:
    """
    Bir yıllık ekonomik adım.
    
    Mantık sırası önemlidir: faiz → enflasyon → tüketim/yatırım → GDP → işsizlik → kur
    
    shock: Dışsal şok uygula, örn: {"inflation": +20, "interest_rate": +5}
    """
    s = copy.deepcopy(state)
    s.year += 1

    # 1. Dışsal şok varsa uygula
    if shock:
        s.inflation      += shock.get("inflation", 0)
        s.interest_rate  += shock.get("interest_rate", 0)
        s.gdp            += shock.get("gdp", 0)

    # 2. Faiz → Enflasyon (para politikasının etkisi)
    # Yüksek faiz kredi maliyetini artırır, talebi düşürür, enflasyonu frenler
    rate_effect = (s.interest_rate - 10) * P.INTEREST_TO_INFLATION
    s.inflation = s.inflation * (1 - rate_effect)
    s.inflation = clamp(s.inflation, P.MIN_INFLATION, P.MAX_INFLATION)

    # 3. Enflasyon → Tüketim
    # Yüksek enflasyon reel satın alma gücünü düşürür
    s.consumption *= (P.TREND_GROWTH - s.inflation * P.INFLATION_TO_CONSUMPTION)
    s.consumption = max(s.consumption, 1.0)

    # 4. Faiz → Yatırım
    # Yüksek faiz yatırım maliyetini artırır, sermaye oluşumunu yavaşlatır
    s.investment *= (P.TREND_GROWTH - s.interest_rate * P.INTEREST_TO_INVESTMENT)
    s.investment = max(s.investment, 1.0)

    # 5. GDP kimliği (harcama yaklaşımı, sadeleştirilmiş)
    # GDP = C + I + G + NX — şimdilik G ve NX sabit katsayıyla dahil
    government_net_exports_factor = 1.25
    s.gdp = (s.consumption + s.investment) * government_net_exports_factor

    # 6. İşsizlik (ters Phillips eğrisi yaklaşımı)
    # Yüksek enflasyon → kısa vadede düşük işsizlik, uzun vadede yapısal sorunlar
    inflation_delta = s.inflation - 20  # 20% eşiğinin üzerindeki enflasyon işsizliği artırır
    s.unemployment += inflation_delta * P.INFLATION_TO_UNEMPLOYMENT
    s.unemployment = clamp(s.unemployment, P.MIN_UNEMPLOYMENT, P.MAX_UNEMPLOYMENT)

    # 7. Döviz kuru (Satın Alma Gücü Paritesi yaklaşımı)
    # TL, enflasyon ile değer kaybeder; faiz kısmen frenler
    effective_inflation = max(0, s.inflation - 3)  # ABD enflasyonu farkı ~3%
    interest_carry = max(0, (s.interest_rate - s.inflation) * 0.05)  # carry trade etkisi
    depreciation = effective_inflation * P.CURRENCY_INFLATION_PASS_THROUGH / 100
    s.currency_usd_try *= (1 + depreciation - interest_carry)
    s.currency_usd_try = max(s.currency_usd_try, 1.0)

    return s


def run_simulation(
    initial_state: TurkeyState,
    years: int = 10,
    shocks: Optional[dict] = None  # {year_offset: shock_dict}
) -> List[TurkeyState]:
    """
    Çok yıllı simülasyon çalıştır.
    
    shocks: Belirli yıllarda şok uygula
    Örnek: {3: {"inflation": 20}, 7: {"interest_rate": -10}}
    """
    history = [initial_state]
    current = initial_state
    shocks = shocks or {}

    for i in range(1, years + 1):
        shock = shocks.get(i)
        current = step(current, shock=shock)
        history.append(current)

    return history
