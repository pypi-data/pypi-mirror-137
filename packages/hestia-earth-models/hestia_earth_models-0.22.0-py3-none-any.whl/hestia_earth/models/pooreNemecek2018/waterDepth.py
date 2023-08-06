from hestia_earth.schema import MeasurementStatsDefinition, SiteSiteType

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.measurement import _new_measurement
from hestia_earth.models.utils.site import WATER_TYPES
from . import MODEL

TERM_ID = 'waterDepth'
SITE_TYPE_TO_DEPTH = {
    SiteSiteType.POND.value: 1.5,
    SiteSiteType.RIVER_OR_STREAM.value: 1,
    SiteSiteType.LAKE.value: 20,
    SiteSiteType.SEA_OR_OCEAN.value: 40
}


def measurement(value: float):
    measurement = _new_measurement(TERM_ID, MODEL)
    measurement['value'] = [value]
    measurement['statsDefinition'] = MeasurementStatsDefinition.MODELLED.value
    return measurement


def _run(site: dict):
    site_type = site.get('siteType')
    value = SITE_TYPE_TO_DEPTH.get(site_type, 0)
    return measurement(value) if value else None


def _should_run(site: dict):
    site_type = site.get('siteType')

    logRequirements(model=MODEL, term=TERM_ID,
                    site_type=site_type)

    should_run = site_type in WATER_TYPES
    logShouldRun(MODEL, TERM_ID, should_run)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else None
