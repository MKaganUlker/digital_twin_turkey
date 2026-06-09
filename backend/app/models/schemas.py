from pydantic import BaseModel


class SimulationResponse(BaseModel):
    year: int
    gdp: float
    inflation: float
    interest_rate: float
    unemployment: float
    currency_usd_try: float