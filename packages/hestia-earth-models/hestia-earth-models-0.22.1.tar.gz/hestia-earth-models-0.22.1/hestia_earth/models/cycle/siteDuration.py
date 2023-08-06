from hestia_earth.models.log import logRequirements, logShouldRun
from . import MODEL

MODEL_KEY = 'siteDuration'


def _run(cycle: dict): return cycle.get('cycleDuration')


def _should_run(cycle: dict):
    cycleDuration = cycle.get('cycleDuration', 0)
    has_other_sites = len(cycle.get('otherSites', [])) == 0

    logRequirements(model=MODEL, key=MODEL_KEY,
                    cycleDuration=cycleDuration,
                    has_other_sites=has_other_sites)

    should_run = all([cycleDuration > 0, has_other_sites])
    logShouldRun(MODEL, None, should_run, key=MODEL_KEY)
    return should_run


def run(cycle: dict): return _run(cycle) if _should_run(cycle) else None
