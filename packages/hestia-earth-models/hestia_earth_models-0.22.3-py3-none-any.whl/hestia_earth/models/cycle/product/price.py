from hestia_earth.schema import TermTermType
from hestia_earth.utils.lookup import (
    get_table_value, column_name, download_lookup, extract_grouped_data, extract_grouped_data_closest_date
)
from hestia_earth.utils.tools import non_empty_list, safe_parse_float, safe_parse_date

from hestia_earth.models.log import debugMissingLookup, debugRequirements, logRequirements, logShouldRun
from hestia_earth.models.utils.cycle import default_currency
from hestia_earth.models.utils.crop import FAOSTAT_PRODUCTION_LOOKUP_COLUMN, get_crop_grouping_faostat_production
from hestia_earth.models.utils.animalProduct import FAO_LOOKUP_COLUMN, get_animalProduct_grouping_fao
from .. import MODEL

MODEL_KEY = 'price'
LOOKUP_NAME = {
    TermTermType.CROP.value: f"region-{TermTermType.CROP.value}-{FAOSTAT_PRODUCTION_LOOKUP_COLUMN}-price.csv",
    TermTermType.ANIMALPRODUCT.value: f"region-{TermTermType.ANIMALPRODUCT.value}-{FAO_LOOKUP_COLUMN}-price.csv"
}
LOOKUP_GROUPING = {
    TermTermType.CROP.value: get_crop_grouping_faostat_production,
    TermTermType.ANIMALPRODUCT.value: get_animalProduct_grouping_fao
}


def _product(product: dict, value: float, currency: str):
    # divide by 1000 to convert price per tonne to kg
    value = value / 1000
    # currency is required, but do not override if present
    return {'currency': currency, **product, MODEL_KEY: value}


def _run(currency: str, product: dict, country_id: str, year: int):
    product_term = product.get('term', {})
    term_id = product_term.get('@id')
    term_type = product_term.get('termType')

    # get the grouping used in region lookup
    grouping = LOOKUP_GROUPING.get(term_type, lambda *_: None)(MODEL, product_term)

    debugRequirements(model=MODEL, term=term_id,
                      grouping=grouping)

    lookup_name = LOOKUP_NAME.get(term_type)
    lookup = download_lookup(lookup_name)
    price_data = get_table_value(lookup, 'termid', country_id, column_name(grouping)) if grouping else None
    debugMissingLookup(lookup_name, 'termid', country_id, grouping, price_data,
                       model=MODEL, term=term_id, key=MODEL_KEY)
    avg_price = extract_grouped_data(price_data, 'Average_price_per_tonne') if (
        price_data and 'Average_price_per_tonne' in price_data
    ) else extract_grouped_data_closest_date(price_data, year)
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
    end_date = safe_parse_date(cycle.get('endDate'))
    year = end_date.year if end_date else None

    logRequirements(model=MODEL, key=MODEL_KEY,
                    country_id=country_id,
                    year=year)

    should_run = all([country_id is not None, year])
    logShouldRun(MODEL, None, should_run, key=MODEL_KEY)
    return should_run, country_id, year


def run(cycle: dict):
    should_run, country_id, year = _should_run(cycle)
    products = list(filter(_should_run_product, cycle.get('products', []))) if should_run else []
    return non_empty_list(map(lambda p: _run(default_currency(cycle), p, country_id, year), products))
