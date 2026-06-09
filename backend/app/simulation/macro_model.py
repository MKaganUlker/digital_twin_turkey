from copy import deepcopy

from app.models.state import TurkeyState
from app.simulation.parameters import *


def step(state: TurkeyState) -> TurkeyState:
    state = deepcopy(state)

    rate_effect = (state.interest_rate - 10) * INTEREST_TO_INFLATION

    state.inflation *= max(
        0.5,
        (1 - rate_effect),
    )

    state.consumption *= (
        TREND_GROWTH
        - state.inflation * INFLATION_TO_CONSUMPTION
    )

    state.investment *= (
        TREND_GROWTH
        - state.interest_rate * INTEREST_TO_INVESTMENT
    )

    state.gdp = (
        state.consumption +
        state.investment
    ) * 1.25

    state.unemployment += (
        state.inflation - 20
    ) * INFLATION_TO_UNEMPLOYMENT / 100

    state.currency_usd_try *= (
        1 + state.inflation / 100 * PASS_THROUGH
    )

    state.year += 1

    return state


def run_simulation(
    initial_state: TurkeyState,
    years: int,
):
    history = []

    state = deepcopy(initial_state)

    for _ in range(years):
        state = step(state)
        history.append(deepcopy(state))

    return history