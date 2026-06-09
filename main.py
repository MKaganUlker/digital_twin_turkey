"""
Digital Twin Türkiye — FastAPI Backend v0.1
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import copy

from .models.state import TurkeyState, INITIAL_STATE
from .simulation.macro_model import run_simulation

app = FastAPI(
    title="Digital Twin Türkiye API",
    description="Türkiye makroekonomik simülasyon motoru",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "version": "0.1.0", "project": "Digital Twin Türkiye"}


@app.get("/simulate", response_model=List[dict])
def simulate(
    years: int = Query(default=10, ge=1, le=50, description="Simülasyon yıl sayısı"),
    interest_override: Optional[float] = Query(default=None, description="Başlangıç faiz oranını override et"),
    inflation_override: Optional[float] = Query(default=None, description="Başlangıç enflasyonu override et"),
):
    """
    Türkiye ekonomisini belirtilen yıl sayısı kadar simüle et.
    
    Opsiyonel olarak başlangıç faiz veya enflasyonu değiştirebilirsin:
    - /simulate?years=10&interest_override=30
    - /simulate?years=15&inflation_override=40
    """
    initial = copy.deepcopy(INITIAL_STATE)

    if interest_override is not None:
        initial.interest_rate = interest_override
    if inflation_override is not None:
        initial.inflation = inflation_override

    history = run_simulation(initial, years=years)
    return [state.to_dict() for state in history]


@app.get("/simulate/shock", response_model=List[dict])
def simulate_with_shock(
    years: int = Query(default=10, ge=1, le=50),
    shock_year: int = Query(default=3, ge=1, le=20, description="Kaçıncı yılda şok uygulanacak"),
    shock_inflation: float = Query(default=0.0, description="Enflasyon şoku (+ veya -)"),
    shock_interest: float = Query(default=0.0, description="Faiz şoku (+ veya -)"),
):
    """
    Belirli bir yılda dışsal ekonomik şok uygulayarak simülasyon yap.
    
    Örnek: Yıl 3'te enflasyon +20 puan şoku
    /simulate/shock?shock_year=3&shock_inflation=20
    """
    shocks = {
        shock_year: {
            "inflation": shock_inflation,
            "interest_rate": shock_interest,
        }
    }
    history = run_simulation(INITIAL_STATE, years=years, shocks=shocks)
    return [state.to_dict() for state in history]


@app.get("/real-data/latest")
def get_latest_real_data():
    """
    TCMB + TÜİK son veri snapshot'ı.
    v0.1'de mock data; v0.2'de gerçek API'ye bağlanacak.
    """
    return {
        "source": "mock (TCMB + TÜİK yaklaşık değerleri)",
        "as_of": "2023-Q4",
        "data": INITIAL_STATE.to_dict(),
        "notes": {
            "gdp": "TÜİK nominal GDP tahmini (milyar TL)",
            "inflation": "TÜFE yıllık % değişim",
            "interest_rate": "TCMB 1 haftalık repo faizi",
            "unemployment": "TÜİK işsizlik oranı",
            "currency_usd_try": "TCMB dolar/TL kuru",
        }
    }


@app.get("/simulate/scenarios")
def compare_scenarios():
    """
    3 farklı senaryo karşılaştırması:
    - Baz senaryo (mevcut politika)
    - Sıkı para politikası (faiz +15)
    - Gevşek para politikası (faiz -20)
    """
    base = run_simulation(INITIAL_STATE, years=10)

    tight_state = copy.deepcopy(INITIAL_STATE)
    tight_state.interest_rate = INITIAL_STATE.interest_rate + 15
    tight = run_simulation(tight_state, years=10)

    loose_state = copy.deepcopy(INITIAL_STATE)
    loose_state.interest_rate = max(5, INITIAL_STATE.interest_rate - 20)
    loose = run_simulation(loose_state, years=10)

    return {
        "base": [s.to_dict() for s in base],
        "tight_monetary": [s.to_dict() for s in tight],
        "loose_monetary": [s.to_dict() for s in loose],
    }
