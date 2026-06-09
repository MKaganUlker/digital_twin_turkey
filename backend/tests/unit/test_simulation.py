from app.services.simulation_service import SimulationService


def test_simulation_runs():
    service = SimulationService()

    result = service.simulate(5)

    assert len(result) == 5