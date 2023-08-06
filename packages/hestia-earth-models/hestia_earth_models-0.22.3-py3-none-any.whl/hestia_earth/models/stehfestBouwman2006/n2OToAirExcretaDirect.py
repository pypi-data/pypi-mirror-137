from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.cycle import get_excreta_N_total
from hestia_earth.models.utils.emission import _new_emission
from .n2OToAirSoilFlux import _get_value, _should_run
from . import MODEL

TERM_ID = 'n2OToAirExcretaDirect'
TIER = EmissionMethodTier.TIER_2.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(cycle: dict, content_list_of_items: list, N_total: float):
    n2OToAirSoilFlux = _get_value(content_list_of_items, N_total)
    value = get_excreta_N_total(cycle)
    logRequirements(model=MODEL, term=TERM_ID,
                    noxToAirSoilFlux=n2OToAirSoilFlux,
                    N_total=value)
    return [_emission(value * n2OToAirSoilFlux / N_total)]


def run(cycle: dict):
    should_run, N_total, content_list_of_items = _should_run(cycle, TERM_ID, TIER)
    logShouldRun(MODEL, TERM_ID, should_run, methodTier=TIER)
    return _run(cycle, content_list_of_items, N_total) if should_run else []
