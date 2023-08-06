from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition

from hestia_earth.models.log import logRequirements
from hestia_earth.models.utils.emission import _new_emission
from .noxToAirSoilFlux import _should_run, _get_value
from . import MODEL

TERM_ID = 'noxToAirCropResidueDecomposition'
TIER = EmissionMethodTier.TIER_1.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(country_id: str, N_total: float, residue: float):
    noxToAirSoilFlux = _get_value(country_id, N_total)
    logRequirements(model=MODEL, term=TERM_ID,
                    noxToAirSoilFlux=noxToAirSoilFlux)
    return [_emission(residue * noxToAirSoilFlux / N_total)]


def run(cycle: dict):
    should_run, country_id, N_total, residue = _should_run(cycle, TERM_ID, TIER)
    return _run(country_id, N_total, residue) if should_run else []
