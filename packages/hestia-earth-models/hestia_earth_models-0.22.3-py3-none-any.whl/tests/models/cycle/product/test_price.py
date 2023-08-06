import json
from tests.utils import fixtures_path

from hestia_earth.models.cycle.product.price import MODEL, MODEL_KEY, run, _should_run, _should_run_product

class_path = f"hestia_earth.models.{MODEL}.product.{MODEL_KEY}"
fixtures_folder = f"{fixtures_path}/{MODEL}/product/{MODEL_KEY}"


def test_should_run():
    cycle = {'endDate': '2020-01'}
    should_run, *_ = _should_run(cycle)
    assert not should_run

    cycle['site'] = {'country': {'@id': 'GADM-GBR'}}
    should_run, *_ = _should_run(cycle)
    assert should_run is True


def test_should_run_product():
    product = {'@type': 'Product'}
    assert not _should_run_product(product)

    product['value'] = [1]
    assert _should_run_product(product) is True

    product['price'] = 2
    assert not _should_run_product(product)


def test_run_crop():
    with open(f"{fixtures_folder}/crop/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/crop/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected


def test_run_animalProduct():
    with open(f"{fixtures_folder}/animalProduct/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/animalProduct/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
