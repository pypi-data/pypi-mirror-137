from hestia_earth.utils.tools import non_empty_list, list_average

from hestia_earth.models.utils.measurement import _new_measurement

MODEL_KEY = 'value'


def _run(measurement: dict):
    value = list_average(measurement.get('min') + measurement.get('max'))
    measurement = _new_measurement(measurement.get('term'))
    measurement[MODEL_KEY] = [value]
    return measurement


def _should_run(measurement: dict):
    should_run = all([
        len(measurement.get(MODEL_KEY, [])) == 0,
        len(measurement.get('min', [])) > 0,
        len(measurement.get('max', [])) > 0
    ])
    return should_run


def run(cycle: dict):
    measurements = list(filter(_should_run, cycle.get('measurements', [])))
    return non_empty_list(map(_run, measurements))
