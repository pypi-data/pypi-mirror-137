from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.cycle import land_occupation_per_ha
from .utils import get_emission_factor
from . import MODEL

TERM_ID = 'co2ToAirSoilCarbonStockChange'
TIER = EmissionMethodTier.TIER_1.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(land_occupation: float, co2_land_use_change: float):
    value = land_occupation * co2_land_use_change
    return [_emission(value)]


def _should_run(cycle: dict):
    land_occupation = land_occupation_per_ha(MODEL, TERM_ID, cycle)
    co2_land_use_change = get_emission_factor(cycle, 'co2LandUseChange')

    logRequirements(model=MODEL, term=TERM_ID,
                    land_occupation=land_occupation,
                    co2_land_use_change=co2_land_use_change)

    should_run = all([land_occupation, co2_land_use_change is not None])
    logShouldRun(MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, land_occupation, co2_land_use_change


def run(cycle: dict):
    should_run, land_occupation, co2_land_use_change = _should_run(cycle)
    return _run(land_occupation, co2_land_use_change) if should_run else []
