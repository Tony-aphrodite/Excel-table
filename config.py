"""
Configuration settings for Spanish Municipalities Excel Generator
"""
import os
import sys

def get_base_path():
    """Get base path - works for both script and PyInstaller .exe"""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller .exe
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_app_path():
    """Get application path (where .exe is located) for output files"""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller .exe - use .exe directory
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Base directory (for bundled resources)
BASE_DIR = get_base_path()

# Data directory (for output files - next to .exe)
DATA_DIR = os.path.join(get_app_path(), "data")

# Classification threshold
POPULATION_THRESHOLD = 2000  # Below this = 100% Rural, Above = Fixed 2000 Rural + rest Urban

# Minimum rural population for urban municipalities
MIN_RURAL_POPULATION = 2000  # Fixed rural population when total >= threshold

# Classification labels (in Spanish)
LABEL_RURAL = "Núcleo Rural"
LABEL_URBAN = "Núcleo Urbano"

# Output file names
OUTPUT_FULL_EXCEL = os.path.join(DATA_DIR, "municipios_espana_completo.xlsx")
OUTPUT_SIMPLE_EXCEL = os.path.join(DATA_DIR, "municipios_espana_clasificacion.xlsx")
OUTPUT_WORD = os.path.join(DATA_DIR, "municipios_espana_clasificacion.docx")

# Wikipedia settings
WIKIPEDIA_API_URL = "https://es.wikipedia.org/w/api.php"
WIKIPEDIA_BASE_URL = "https://es.wikipedia.org/wiki/"

# Rate limiting (seconds between requests)
# Note: Parallel processing uses MAX_WORKERS instead of delay
REQUEST_DELAY = 0.5

# User agent for requests (Wikipedia requires descriptive User-Agent)
# Format: AppName/Version (Contact Info) Framework/Version
USER_AGENT = "MunicipiosGenerator/1.0 (Municipal Data Educational Tool; Python/requests) Python-requests/2.28"

# Spanish provinces list
SPANISH_PROVINCES = [
    "A Coruña", "Álava", "Albacete", "Alicante", "Almería", "Asturias",
    "Ávila", "Badajoz", "Barcelona", "Bizkaia", "Burgos", "Cáceres",
    "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca",
    "Gipuzkoa", "Girona", "Granada", "Guadalajara", "Huelva", "Huesca",
    "Illes Balears", "Jaén", "La Rioja", "Las Palmas", "León", "Lleida",
    "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", "Palencia",
    "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia", "Sevilla",
    "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid",
    "Zamora", "Zaragoza"
]

# Equipment calculation divisors (different for urban and rural)
EQUIPMENT_DIVISOR_URBAN = 300  # Urban: Population / 300
EQUIPMENT_DIVISOR_RURAL = 50   # Rural: Population / 50

# Default urban percentage for municipalities classified as urban
# (used when exact data is not available)
# Based on typical Spanish urban municipalities: ~95% urban, ~5% rural
DEFAULT_URBAN_PERCENTAGE = 0.95

# Column names for Excel (in Spanish)
COLUMN_NAMES = {
    "name": "Municipio",
    "total_hab": "TOTAL HAB",
    "hab_urban": "Nº HAB URBANO",
    "hab_rural": "Nº HAB RURAL",
    "equipos_urban": "EQUIPOS URBANO",
    "equipos_rural": "EQUIPOS RURAL",
    "total_equipos": "TOTAL EQUIPOS"
}

# Simple output columns (first and last)
SIMPLE_COLUMNS = {
    "name": "Municipio",
    "total_equipos": "TOTAL EQUIPOS"
}
