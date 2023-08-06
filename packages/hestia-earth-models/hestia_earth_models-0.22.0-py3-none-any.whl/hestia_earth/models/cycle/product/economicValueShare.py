from hestia_earth.schema import TermTermType
from hestia_earth.utils.tools import safe_parse_float
from hestia_earth.utils.model import filter_list_term_type, find_primary_product

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.cycle import unique_currencies
from hestia_earth.models.utils.term import get_lookup_value
from .. import MODEL

MODEL_KEY = 'economicValueShare'


def _product(product: dict, value: float):
    return {**product, MODEL_KEY: value}


def _run_by_revenue(products: list):
    total_revenue = sum([p.get('revenue', 0) for p in products])
    return [_product(p, p.get('revenue', 0) / total_revenue * 100) for p in products if p.get('revenue') > 0]


def _lookup_share(product: dict, default=None):
    return safe_parse_float(
        get_lookup_value(product.get('term', {}), 'global_economic_value_share', model=MODEL, key=MODEL_KEY), default)


def _run_by_product(product: dict):
    value = _lookup_share(product)
    return [] if value is None else [_product(product, value)]


def _should_run_single(cycle: dict):
    values = [(p, _lookup_share(p, 0)) for p in cycle.get('products', [])]
    products = [p for p, value in values if value != 0]
    product = (products[0] if len(products) == 1 else {})
    term_id = product.get('term', {}).get('@id')
    not_already_set = MODEL_KEY not in product.keys()
    single_product = term_id is not None

    logRequirements(model=MODEL, term=term_id, key=MODEL_KEY,
                    single_product=single_product,
                    not_already_set=not_already_set)

    should_run = all([single_product, not_already_set])
    logShouldRun(MODEL, None, should_run, key=MODEL_KEY, by='single')
    return should_run, product if should_run else None


def _run_by_single(cycle: dict):
    should_run_single, single_product = _should_run_single(cycle)
    return [_product(single_product, 100)] if should_run_single else []


def _should_run_by_product(cycle: dict):
    primary_product = find_primary_product(cycle) or {}
    term_id = primary_product.get('term', {}).get('@id')
    product_is_crop = primary_product.get('term', {}).get('termType') == TermTermType.CROP.value
    single_product_crop = len(filter_list_term_type(cycle.get('products', []), TermTermType.CROP)) == 1
    not_already_set = MODEL_KEY not in primary_product.keys()

    logRequirements(model=MODEL, term=term_id, key=MODEL_KEY,
                    product_is_crop=product_is_crop,
                    single_product_crop=single_product_crop,
                    not_already_set=not_already_set)

    should_run = all([product_is_crop, single_product_crop, not_already_set])
    logShouldRun(MODEL, term_id, should_run, key=MODEL_KEY, by='product')
    return should_run


def _should_have_revenue(product: dict):
    term_type = product.get('term', {}).get('termType')
    return term_type not in [
        TermTermType.CROPRESIDUE.value,
        TermTermType.EXCRETA.value
    ]


def _should_run_by_revenue(cycle: dict):
    products = cycle.get('products', [])
    total_value = sum([p.get(MODEL_KEY, 0) for p in products])
    currencies = unique_currencies(cycle)
    same_currencies = len(currencies) < 2
    all_with_revenue = all([p.get('revenue', -1) >= 0 for p in products if _should_have_revenue(p)])

    logRequirements(model=MODEL, key=MODEL_KEY,
                    total_value=total_value,
                    all_with_revenue=all_with_revenue,
                    currencies=';'.join(currencies),
                    same_currencies=same_currencies)

    should_run = all([total_value < 100.5, all_with_revenue, same_currencies])
    logShouldRun(MODEL, None, should_run, key=MODEL_KEY, by='revenue')
    return should_run


def run(cycle: dict):
    products = cycle.get('products', [])
    return _run_by_revenue(products) if _should_run_by_revenue(cycle) else (
        _run_by_product(find_primary_product(cycle)) if _should_run_by_product(cycle) else _run_by_single(cycle)
    )
