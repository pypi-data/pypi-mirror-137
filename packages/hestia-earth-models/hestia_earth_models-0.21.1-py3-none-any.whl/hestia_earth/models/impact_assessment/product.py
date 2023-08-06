from hestia_earth.utils.model import find_primary_product

from hestia_earth.models.log import logShouldRun
from . import MODEL

MODEL_KEY = 'product'


def _should_run(impact: dict):
    primary_product = find_primary_product(impact.get('cycle', {}))
    should_run = primary_product is not None
    logShouldRun(MODEL, None, should_run, key=MODEL_KEY)
    return should_run, primary_product


def run(impact: dict):
    should_run, primary_product = _should_run(impact)
    return primary_product.get('term', {}) if should_run else None
