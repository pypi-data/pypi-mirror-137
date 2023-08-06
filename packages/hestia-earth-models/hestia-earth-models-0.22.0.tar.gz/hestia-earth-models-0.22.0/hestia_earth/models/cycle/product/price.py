from hestia_earth.utils.lookup import get_table_value, column_name, download_lookup, extract_grouped_data
from hestia_earth.utils.tools import non_empty_list, safe_parse_float

from hestia_earth.models.log import debugMissingLookup, debugRequirements, logRequirements, logShouldRun
from hestia_earth.models.utils.cycle import default_currency
from hestia_earth.models.utils.crop import FAOSTAT_PRODUCTION_LOOKUP_COLUMN, get_crop_grouping_faostat_production
from .. import MODEL

MODEL_KEY = 'price'
LOOKUP_NAME = f"region-crop-{FAOSTAT_PRODUCTION_LOOKUP_COLUMN}-price.csv"


def _product(product: dict, value: float, currency: str):
    # divide by 1000 to convert price per tonne to kg
    value = value / 1000
    # currency is required, but do not override if present
    return {'currency': currency, **product, MODEL_KEY: value}


def _run(cycle: dict, currency: str, product: dict):
    # get the grouping used in region lookup
    grouping = get_crop_grouping_faostat_production(product.get('term', {}))

    # based on annual value averaged between 1991-2018, source: FAOSTAT
    lookup = download_lookup(LOOKUP_NAME)
    country_id = cycle.get('site', {}).get('country', {}).get('@id')
    term_id = product.get('term', {}).get('@id', '')
    debugRequirements(model=MODEL, term=term_id,
                      country=country_id,
                      grouping=grouping)
    price_data = get_table_value(lookup, 'termid', country_id, column_name(grouping)) if grouping else None
    debugMissingLookup(LOOKUP_NAME, 'termid', country_id, grouping, price_data,
                       model=MODEL, term=term_id, key=MODEL_KEY)
    avg_price = extract_grouped_data(price_data, 'Average_price_per_tonne')
    value = safe_parse_float(avg_price, None)
    return None if value is None else _product(product, value, currency)


def _should_run_product(product: dict):
    term_id = product.get('term', {}).get('@id')
    has_yield = len(product.get('value', [])) > 0
    not_already_set = MODEL_KEY not in product.keys()

    logRequirements(model=MODEL, term=term_id, key=MODEL_KEY,
                    has_yield=has_yield,
                    not_already_set=not_already_set)

    should_run = all([not_already_set, has_yield])
    logShouldRun(MODEL, term_id, should_run, key=MODEL_KEY)
    return should_run


def _should_run(cycle: dict):
    country_id = cycle.get('site', {}).get('country', {}).get('@id')
    should_run = country_id is not None
    logShouldRun(MODEL, None, should_run, key=MODEL_KEY)
    return should_run


def run(cycle: dict):
    should_run = _should_run(cycle)
    products = list(filter(_should_run_product, cycle.get('products', []))) if should_run else []
    return non_empty_list(map(lambda p: _run(cycle, default_currency(cycle), p), products))
