"""
Country configurations for Multi-Country Municipality Generator
"""
from .spain import SPAIN_CONFIG
from .france import FRANCE_CONFIG
from .italy import ITALY_CONFIG
from .portugal import PORTUGAL_CONFIG
from .germany import GERMANY_CONFIG

# Available countries
COUNTRY_CONFIGS = {
    "España": SPAIN_CONFIG,
    "France": FRANCE_CONFIG,
    "Italia": ITALY_CONFIG,
    "Portugal": PORTUGAL_CONFIG,
    "Deutschland": GERMANY_CONFIG,
}

def get_country_config(country_name):
    """Get configuration for a specific country"""
    return COUNTRY_CONFIGS.get(country_name)

def get_available_countries():
    """Get list of available countries"""
    return list(COUNTRY_CONFIGS.keys())
