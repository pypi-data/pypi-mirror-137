from hestia_earth.utils.tools import non_empty_list, list_average

MODEL_KEY = 'value'


def _run(input: dict):
    value = list_average(input.get('min') + input.get('max'))
    return {**input, MODEL_KEY: [value]}


def _should_run(input: dict):
    should_run = all([
        len(input.get(MODEL_KEY, [])) == 0,
        len(input.get('min', [])) > 0,
        len(input.get('max', [])) > 0
    ])
    return should_run


def run(cycle: dict):
    inputs = list(filter(_should_run, cycle.get('inputs', [])))
    return non_empty_list(map(_run, inputs))
