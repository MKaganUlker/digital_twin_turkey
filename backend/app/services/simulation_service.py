from app.models.state import TurkeyState
from app.simulation.macro_model import run_simulation


class SimulationService:

    def simulate(self, years: int):
        initial = TurkeyState(
            year=2023,
            gdp=21000,

            inflation=52.0,
            interest_rate=42.5,
            unemployment=8.8,

            currency_usd_try=38.0,

            consumption=12000,
            investment=5000,
        )

        return run_simulation(
            initial,
            years,
        )