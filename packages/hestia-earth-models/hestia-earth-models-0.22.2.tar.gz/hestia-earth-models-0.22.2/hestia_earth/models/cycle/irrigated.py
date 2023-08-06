from hestia_earth.schema import TermTermType, CycleFunctionalUnit
from hestia_earth.utils.tools import list_average
from hestia_earth.utils.model import filter_list_term_type

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.practice import _new_practice
from . import MODEL

TERM_ID = 'irrigated'


def _run(): return [_new_practice(TERM_ID)]


def _has_water_practices(practices: list):
    return not any([p for p in practices if p.get('term', {}).get('termType') == TermTermType.WATERREGIME.value
                    and p.get('term', {}).get('@id') != TERM_ID])


def _should_run(cycle: dict):
    functional_unit = cycle.get('functionalUnit')
    has_water_practices = _has_water_practices(cycle.get('practices', []))
    irrigation_inputs = filter_list_term_type(cycle.get('inputs', []), TermTermType.WATER)
    has_irrigation_inputs = len(irrigation_inputs) > 0
    irrigation_value = sum([list_average(i.get('value')) for i in irrigation_inputs if len(i.get('value', [])) > 0])

    logRequirements(model=MODEL, term=TERM_ID,
                    functional_unit=functional_unit,
                    has_water_practices=has_water_practices,
                    has_irrigation_inputs=has_irrigation_inputs,
                    irrigation_value=irrigation_value)

    should_run = all([
        has_water_practices,
        has_irrigation_inputs,
        functional_unit != CycleFunctionalUnit._1_HA.value or irrigation_value > 250
    ])
    logShouldRun(MODEL, TERM_ID, should_run)
    return should_run


def run(cycle: dict): return _run() if _should_run(cycle) else []
