"""
Italy country configuration
Uses REGIONS instead of provinces for Wikipedia scraping
"""

ITALY_CONFIG = {
    "name": "Italia",
    "language": "it",
    "wikipedia_api": "https://it.wikipedia.org/w/api.php",
    "wikipedia_base": "https://it.wikipedia.org/wiki/",

    # Labels in local language
    "labels": {
        "municipality": "Comune",
        "total_hab": "TOTALE AB",
        "hab_urban": "Nº AB URBANO",
        "hab_rural": "Nº AB RURALE",
        "equipos_urban": "SQUADRE URBANO",
        "equipos_rural": "SQUADRE RURALE",
        "total_equipos": "TOTALE SQUADRE",
        "rural": "Zona Rurale",
        "urban": "Zona Urbana",
    },

    # Italian REGIONS (not provinces) - matches Wikipedia page structure
    "regions": [
        "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
        "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche",
        "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia",
        "Toscana", "Trentino-Alto Adige", "Umbria", "Valle d'Aosta", "Veneto"
    ],

    # Page title pattern for Italian Wikipedia (using regions)
    "page_title_pattern": "Comuni_{region}",
    "default_region_pattern": "della_{region}",

    # Region mappings for proper Italian articles
    "region_page_mappings": {
        # dell' for vowels
        "Abruzzo": "Comuni_dell'Abruzzo",
        "Emilia-Romagna": "Comuni_dell'Emilia-Romagna",
        "Umbria": "Comuni_dell'Umbria",
        # della for feminine
        "Basilicata": "Comuni_della_Basilicata",
        "Calabria": "Comuni_della_Calabria",
        "Campania": "Comuni_della_Campania",
        "Liguria": "Comuni_della_Liguria",
        "Lombardia": "Comuni_della_Lombardia",
        "Puglia": "Comuni_della_Puglia",
        "Sardegna": "Comuni_della_Sardegna",
        "Sicilia": "Comuni_della_Sicilia",
        "Toscana": "Comuni_della_Toscana",
        # del for masculine
        "Friuli-Venezia Giulia": "Comuni_del_Friuli-Venezia_Giulia",
        "Lazio": "Comuni_del_Lazio",
        "Molise": "Comuni_del_Molise",
        "Piemonte": "Comuni_del_Piemonte",
        "Trentino-Alto Adige": "Comuni_del_Trentino-Alto_Adige",
        "Veneto": "Comuni_del_Veneto",
        # delle for plural feminine
        "Marche": "Comuni_delle_Marche",
        # Special case
        "Valle d'Aosta": "Comuni_della_Valle_d'Aosta",
    },
}
