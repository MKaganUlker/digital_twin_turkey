from dataclasses import dataclass


@dataclass
class TurkeyState:
    year: int

    gdp: float

    inflation: float
    interest_rate: float
    unemployment: float

    currency_usd_try: float

    consumption: float
    investment: float