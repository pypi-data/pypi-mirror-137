from dateutil.relativedelta import relativedelta
from hestia_earth.utils.date import is_in_days
from hestia_earth.utils.tools import safe_parse_date

from hestia_earth.models.log import logRequirements, logShouldRun
from .. import MODEL

MODEL_KEY = 'startDate'


def _run(cycle: dict):
    days = -float(cycle.get('cycleDuration'))
    return (safe_parse_date(cycle.get('endDate')) + relativedelta(days=days)).strftime('%Y-%m-%d')


def _should_run(cycle: dict):
    has_full_date = is_in_days(cycle.get('endDate'))
    cycleDuration = cycle.get('cycleDuration')

    logRequirements(model=MODEL, key=MODEL_KEY,
                    has_full_date=has_full_date,
                    cycleDuration=cycleDuration)

    should_run = all([
        has_full_date,
        cycleDuration is not None,
        cycle.get(MODEL_KEY) is None
    ])
    logShouldRun(MODEL, None, should_run, key=MODEL_KEY)
    return should_run


def run(cycle: dict): return {**cycle, MODEL_KEY: _run(cycle)} if _should_run(cycle) else cycle
