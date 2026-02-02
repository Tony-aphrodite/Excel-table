"""
Portugal country configuration
"""

PORTUGAL_CONFIG = {
    "name": "Portugal",
    "language": "pt",
    "wikipedia_api": "https://pt.wikipedia.org/w/api.php",
    "wikipedia_base": "https://pt.wikipedia.org/wiki/",

    # Labels in local language
    "labels": {
        "municipality": "Município",
        "total_hab": "TOTAL HAB",
        "hab_urban": "Nº HAB URBANO",
        "hab_rural": "Nº HAB RURAL",
        "equipos_urban": "EQUIPAS URBANO",
        "equipos_rural": "EQUIPAS RURAL",
        "total_equipos": "TOTAL EQUIPAS",
        "rural": "Zona Rural",
        "urban": "Zona Urbana",
    },

    # Portuguese districts
    "regions": [
        "Aveiro", "Beja", "Braga", "Bragança", "Castelo Branco",
        "Coimbra", "Évora", "Faro", "Guarda", "Leiria",
        "Lisboa", "Portalegre", "Porto", "Santarém", "Setúbal",
        "Viana do Castelo", "Vila Real", "Viseu",
        "Região Autónoma dos Açores", "Região Autónoma da Madeira"
    ],

    # Page title pattern for Portuguese Wikipedia
    "page_title_pattern": "Lista_de_municípios_do_distrito_de_{region}",
    "default_region_pattern": "{region}",

    # Region mappings for special cases
    "region_page_mappings": {
        "Região Autónoma dos Açores": "Lista_de_municípios_dos_Açores",
        "Região Autónoma da Madeira": "Lista_de_municípios_da_Madeira",
    },
}
