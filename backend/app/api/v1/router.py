from fastapi import APIRouter

from app.services.simulation_service import SimulationService
from app.services.data_service import DataService

router = APIRouter()

simulation_service = SimulationService()
data_service = DataService()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/simulate")
def simulate(years: int = 10):
    return simulation_service.simulate(years)


@router.get("/real-data/latest")
def latest():
    return data_service.latest_snapshot()