from hestia_earth.schema import TermTermType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data_closest_date
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.animalProduct import (
    FAO_LOOKUP_COLUMN, FAO_EQUIVALENT_LOOKUP_COLUMN, get_animalProduct_lookup_value
)
from hestia_earth.models.utils.product import convert_animalProduct_to_unit
from . import MODEL

LOOKUP_PREFIX = f"{TermTermType.REGION.value}-{TermTermType.ANIMALPRODUCT.value}-{FAO_LOOKUP_COLUMN}"


def product_equivalent_value(product: dict, year: int, country: str):
    term_id = product.get('term', {}).get('@id')
    fao_product_id = get_animalProduct_lookup_value(MODEL, term_id, FAO_EQUIVALENT_LOOKUP_COLUMN)
    grouping = get_animalProduct_lookup_value(MODEL, fao_product_id, FAO_LOOKUP_COLUMN)

    if not grouping or not fao_product_id:
        return None

    lookup = download_lookup(f"{LOOKUP_PREFIX}-productionQuantity.csv")
    quantity_values = get_table_value(lookup, 'termid', country, column_name(grouping))
    quantity = safe_parse_float(extract_grouped_data_closest_date(quantity_values, year))

    lookup = download_lookup(f"{LOOKUP_PREFIX}-head.csv")
    head_values = get_table_value(lookup, 'termid', country, column_name(grouping))
    head = safe_parse_float(extract_grouped_data_closest_date(head_values, year))

    # quantity is in Tonnes
    value = quantity * 1000 / head if head > 0 else 0

    fao_product_term = download_hestia(fao_product_id)
    fao_product = {'term': fao_product_term, 'value': [value]}

    # use the FAO value to convert it to the correct unit
    dest_unit = product.get('term', {}).get('units')
    conv_value = convert_animalProduct_to_unit(fao_product, dest_unit)

    logger.debug('model=%s, quantity=%s, head=%s, value=%s, conv value=%s', MODEL, quantity, head, value, conv_value)

    return conv_value
