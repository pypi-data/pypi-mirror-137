from hestia_earth.schema import IndicatorStatsDefinition

from hestia_earth.models.log import debugRequirements, logRequirements, logShouldRun
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_product, convert_value_from_cycle
from hestia_earth.models.utils.cycle import land_occupation_per_kg
from hestia_earth.models.utils.input import sum_input_impacts
from .utils import get_emission_factor
from . import MODEL

TERM_ID_CYCLE = 'landTransformationFromForest20YearAverageDuringCycle'
TERM_ID_INPUTS = 'landTransformationFromForest20YearAverageInputsProduction'
TERM_ID = 'landTransformationFromForest20YearAverageDuringCycle,landTransformationFromForest20YearAverageInputsProduction'  # noqa: E501


def _indicator(term_id: str, value: float):
    indicator = _new_indicator(term_id, MODEL)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def _run_inputs(impact_assessment: dict, product: dict):
    cycle = impact_assessment.get('cycle', {})
    value = convert_value_from_cycle(product, sum_input_impacts(cycle.get('inputs', []), TERM_ID_CYCLE))
    debugRequirements(model=MODEL, term=TERM_ID_INPUTS,
                      value=value)
    return [_indicator(TERM_ID_INPUTS, value)]


def _run(land_occupation_m2: float, factor: float):
    value = land_occupation_m2 * factor
    debugRequirements(model=MODEL, term=TERM_ID_CYCLE,
                      value=value)
    return _indicator(TERM_ID_CYCLE, value)


def _should_run(impact_assessment: dict):
    cycle = impact_assessment.get('cycle', {})
    product = get_product(impact_assessment)
    land_occupation_m2_kg = land_occupation_per_kg(MODEL, TERM_ID_CYCLE, cycle, product)
    land_transformation_factor = get_emission_factor(cycle, 'landTransformation20YearsAverage')

    logRequirements(model=MODEL, term=TERM_ID,
                    land_occupation_m2_kg=land_occupation_m2_kg,
                    land_transformation_factor=land_transformation_factor)

    should_run = all([land_occupation_m2_kg, land_transformation_factor is not None])
    logShouldRun(MODEL, TERM_ID, should_run)

    should_run_inputs = all([product])
    logShouldRun(MODEL, TERM_ID_INPUTS, should_run_inputs)

    return should_run, should_run_inputs, product, land_occupation_m2_kg, land_transformation_factor


def run(impact_assessment: dict):
    should_run, should_run_inputs, product, land_occupation_m2, factor = _should_run(impact_assessment)
    return (
        [_run(land_occupation_m2, factor)] if should_run else []
    ) + (
        _run_inputs(impact_assessment, product) if should_run_inputs else []
    )
