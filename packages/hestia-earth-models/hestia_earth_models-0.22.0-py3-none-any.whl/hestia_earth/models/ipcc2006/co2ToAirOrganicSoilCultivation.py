from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.measurement import most_relevant_measurement_value
from hestia_earth.models.utils.ecoClimateZone import get_ecoClimateZone_lookup_value
from hestia_earth.models.utils.cycle import land_occupation_per_ha
from hestia_earth.models.utils.cycle import valid_site_type
from . import MODEL

TERM_ID = 'co2ToAirOrganicSoilCultivation'
TIER = EmissionMethodTier.TIER_1.value
CONVERT_FACTOR = 44 / 120


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(histosol: float, organic_soil_factor: float, land_occupation: float):
    value = land_occupation * histosol / 100 * organic_soil_factor
    return [_emission(value)]


def _get_CO2_factor(eco_climate_zone: str, site_type: str):
    return get_ecoClimateZone_lookup_value(
        eco_climate_zone, 'IPCC_2006_ORGANIC_SOILS_TONNES_CO2-C_HECTARE', site_type
    ) * CONVERT_FACTOR


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    site = cycle.get('site', {})
    site_type = site.get('siteType', None)
    site_type_valid = valid_site_type(cycle, True)
    measurements = site.get('measurements', [])

    def _get_measurement_content(term_id: str):
        return most_relevant_measurement_value(measurements, term_id, end_date)

    histosol = _get_measurement_content('histosol') or 0
    eco_climate_zone = _get_measurement_content('ecoClimateZone')
    organic_soil_factor = _get_CO2_factor(eco_climate_zone, site_type) if eco_climate_zone else 0
    land_occupation = land_occupation_per_ha(MODEL, TERM_ID, cycle)

    logRequirements(model=MODEL, term=TERM_ID,
                    site_type_valid=site_type_valid,
                    organic_soil_factor=organic_soil_factor,
                    land_occupation=land_occupation,
                    histosol=histosol)

    should_run = all([site_type_valid, organic_soil_factor, land_occupation])
    logShouldRun(MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, histosol, organic_soil_factor, land_occupation


def run(cycle: dict):
    should_run, histosol, organic_soil_factor, land_occupation = _should_run(cycle)
    return _run(histosol, organic_soil_factor, land_occupation) if should_run else []
