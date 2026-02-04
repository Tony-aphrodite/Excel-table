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

    # Region mappings - German Wikipedia uses various patterns per state
    "region_page_mappings": {
        # Full page titles for each state
        "Baden-Württemberg": "Liste_der_Städte_und_Gemeinden_in_Baden-Württemberg",
        "Bayern": "Liste_der_Gemeinden_in_Bayern",
        "Brandenburg": "Liste_der_Gemeinden_in_Brandenburg",
        "Hessen": "Liste_der_Gemeinden_in_Hessen",
        "Mecklenburg-Vorpommern": "Liste_der_Gemeinden_in_Mecklenburg-Vorpommern",
        "Niedersachsen": "Liste_der_Gemeinden_in_Niedersachsen",
        "Nordrhein-Westfalen": "Liste_der_Gemeinden_in_Nordrhein-Westfalen",
        "Rheinland-Pfalz": "Liste_der_Gemeinden_in_Rheinland-Pfalz",
        "Saarland": "Liste_der_Gemeinden_im_Saarland",
        "Sachsen": "Liste_der_Gemeinden_in_Sachsen",
        "Sachsen-Anhalt": "Liste_der_Gemeinden_in_Sachsen-Anhalt",
        "Schleswig-Holstein": "Liste_der_Gemeinden_in_Schleswig-Holstein",
        "Thüringen": "Liste_der_Gemeinden_in_Thüringen",
        # City-states are single municipalities
        "Berlin": "Liste_der_Bezirke_und_Ortsteile_Berlins",
        "Bremen": "Liste_der_Stadtteile_von_Bremen",
        "Hamburg": "Liste_der_Bezirke_und_Stadtteile_Hamburgs",
    },
}
