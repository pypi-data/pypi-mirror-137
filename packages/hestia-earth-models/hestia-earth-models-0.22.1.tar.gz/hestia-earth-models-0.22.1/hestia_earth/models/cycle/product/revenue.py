from hestia_earth.utils.tools import list_sum, non_empty_list

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.cycle import default_currency
from .. import MODEL

MODEL_KEY = 'revenue'


def _run(currency: str):
    def run(product: dict):
        value = list_sum(product.get('value', [0])) * product.get('price', 0)
        return {'currency': currency, **product, MODEL_KEY: value}
    return run


def _should_run(product: dict):
    term_id = product.get('term', {}).get('@id')
    has_yield = len(product.get('value', [])) > 0
    has_price = product.get('price', 0) > 0
    not_already_set = MODEL_KEY not in product.keys()

    logRequirements(model=MODEL, term=term_id, key=MODEL_KEY,
                    has_yield=has_yield,
                    has_price=has_price,
                    not_already_set=not_already_set)

    should_run = all([
        not_already_set,
        any([
            has_yield and has_price,
            list_sum(product.get('value', []), -1) == 0
        ])
    ])
    logShouldRun(MODEL, term_id, should_run, key=MODEL_KEY)
    return should_run


def run(cycle: dict):
    products = list(filter(_should_run, cycle.get('products', [])))
    return non_empty_list(map(_run(default_currency(cycle)), products))
