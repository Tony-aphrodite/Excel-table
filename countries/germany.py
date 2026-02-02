"""
Germany country configuration
"""

GERMANY_CONFIG = {
    "name": "Deutschland",
    "language": "de",
    "wikipedia_api": "https://de.wikipedia.org/w/api.php",
    "wikipedia_base": "https://de.wikipedia.org/wiki/",

    # Labels in local language
    "labels": {
        "municipality": "Gemeinde",
        "total_hab": "GESAMT EW",
        "hab_urban": "EW STÄDTISCH",
        "hab_rural": "EW LÄNDLICH",
        "equipos_urban": "TEAMS STÄDTISCH",
        "equipos_rural": "TEAMS LÄNDLICH",
        "total_equipos": "GESAMT TEAMS",
        "rural": "Ländlich",
        "urban": "Städtisch",
    },

    # German states (Bundesländer)
    "regions": [
        "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen",
        "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
        "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen",
        "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"
    ],

    # Page title pattern for German Wikipedia
    "page_title_pattern": "Liste_der_Gemeinden_in_{region}",
    "default_region_pattern": "{region}",

    # Region mappings for special cases
    "region_page_mappings": {},
}
