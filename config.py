"""
Configuration settings for Spanish Municipalities Excel Generator
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Classification threshold
POPULATION_THRESHOLD = 3000  # Below this = Rural, Above = Urban

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
REQUEST_DELAY = 0.5

# User agent for requests
USER_AGENT = "MunicipiosSpainBot/1.0 (Educational Project)"

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

# Equipment calculation divisor
EQUIPMENT_DIVISOR = 300  # Population / 300 = Equipment

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
