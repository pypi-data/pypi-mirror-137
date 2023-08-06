from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition
from hestia_earth.utils.tools import list_sum, safe_parse_float

from hestia_earth.models.log import debugRequirements, logRequirements, logShouldRun
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.input import get_total_nitrogen
from hestia_earth.models.utils.product import residue_nitrogen
from hestia_earth.models.utils.cycle import valid_site_type
from . import MODEL

TERM_ID = 'noxToAirSoilFlux'
TIER = EmissionMethodTier.TIER_1.value


def _should_run(cycle: dict, term=TERM_ID, tier=TIER):
    country = cycle.get('site', {}).get('country', {})
    residue = residue_nitrogen(cycle.get('products', []))
    N_total = list_sum(get_total_nitrogen(cycle.get('inputs', [])) + [residue])
    site_type_valid = valid_site_type(cycle)

    logRequirements(model=MODEL, term=term,
                    country=country.get('@id'),
                    residue=residue,
                    N_total=N_total,
                    site_type_valid=site_type_valid)

    should_run = all([site_type_valid, country, N_total > 0])
    logShouldRun(MODEL, term, should_run, methodTier=tier)
    return should_run, country, N_total, residue


def _get_value(country: dict, N_total: float):
    value = safe_parse_float(get_lookup_value(country, 'ef_nox', model=MODEL, term=TERM_ID))
    debugRequirements(model=MODEL, term=TERM_ID,
                      nox=value,
                      N_total=N_total)
    return value * N_total


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(country: dict, N_total: float):
    value = _get_value(country, N_total)
    return [_emission(value)]


def run(cycle: dict):
    should_run, country, N_total, *args = _should_run(cycle)
    return _run(country, N_total) if should_run else []
