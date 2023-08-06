from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition

from hestia_earth.models.log import logRequirements
from hestia_earth.models.utils.input import get_inorganic_fertilizer_N_total
from hestia_earth.models.utils.emission import _new_emission
from .noxToAirSoilFlux import _should_run, _get_value
from . import MODEL

TERM_ID = 'noxToAirInorganicFertilizer'
TIER = EmissionMethodTier.TIER_2.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(cycle: dict, ecoClimateZone: str, nitrogenContent: float, N_total: float):
    noxToAirSoilFlux = _get_value(ecoClimateZone, nitrogenContent, N_total)
    value = get_inorganic_fertilizer_N_total(cycle)
    logRequirements(model=MODEL, term=TERM_ID,
                    noxToAirSoilFlux=noxToAirSoilFlux,
                    N_total=value)
    return [_emission(value * noxToAirSoilFlux / N_total)]


def run(cycle: dict):
    should_run, ecoClimateZone, nitrogenContent, N_total, *args = _should_run(cycle, TERM_ID, TIER)
    return _run(cycle, ecoClimateZone, nitrogenContent, N_total) if should_run else []
