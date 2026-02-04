"""
Italy country configuration
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

    # Italian provinces
    "regions": [
        "Agrigento", "Alessandria", "Ancona", "Aosta", "Arezzo",
        "Ascoli Piceno", "Asti", "Avellino", "Bari", "Barletta-Andria-Trani",
        "Belluno", "Benevento", "Bergamo", "Biella", "Bologna",
        "Bolzano", "Brescia", "Brindisi", "Cagliari", "Caltanissetta",
        "Campobasso", "Carbonia-Iglesias", "Caserta", "Catania", "Catanzaro",
        "Chieti", "Como", "Cosenza", "Cremona", "Crotone",
        "Cuneo", "Enna", "Fermo", "Ferrara", "Firenze",
        "Foggia", "Forlì-Cesena", "Frosinone", "Genova", "Gorizia",
        "Grosseto", "Imperia", "Isernia", "L'Aquila", "La Spezia",
        "Latina", "Lecce", "Lecco", "Livorno", "Lodi",
        "Lucca", "Macerata", "Mantova", "Massa-Carrara", "Matera",
        "Medio Campidano", "Messina", "Milano", "Modena", "Monza e Brianza",
        "Napoli", "Novara", "Nuoro", "Ogliastra", "Olbia-Tempio",
        "Oristano", "Padova", "Palermo", "Parma", "Pavia",
        "Perugia", "Pesaro e Urbino", "Pescara", "Piacenza", "Pisa",
        "Pistoia", "Pordenone", "Potenza", "Prato", "Ragusa",
        "Ravenna", "Reggio Calabria", "Reggio Emilia", "Rieti", "Rimini",
        "Roma", "Rovigo", "Salerno", "Sassari", "Savona",
        "Siena", "Siracusa", "Sondrio", "Taranto", "Teramo",
        "Terni", "Torino", "Trapani", "Trento", "Treviso",
        "Trieste", "Udine", "Varese", "Venezia", "Verbano-Cusio-Ossola",
        "Vercelli", "Verona", "Vibo Valentia", "Vicenza", "Viterbo"
    ],

    # Page title pattern for Italian Wikipedia
    "page_title_pattern": "Comuni_della_provincia_di_{region}",
    "default_region_pattern": "{region}",

    # Region mappings ONLY for special cases that differ from standard pattern
    "region_page_mappings": {
        # Valle d'Aosta - special autonomous region
        "Aosta": "Comuni_della_Valle_d'Aosta",

        # Metropolitan cities use different page pattern
        "Bari": "Comuni_della_città_metropolitana_di_Bari",
        "Bologna": "Comuni_della_città_metropolitana_di_Bologna",
        "Cagliari": "Comuni_della_città_metropolitana_di_Cagliari",
        "Catania": "Comuni_della_città_metropolitana_di_Catania",
        "Firenze": "Comuni_della_città_metropolitana_di_Firenze",
        "Genova": "Comuni_della_città_metropolitana_di_Genova",
        "Messina": "Comuni_della_città_metropolitana_di_Messina",
        "Milano": "Comuni_della_città_metropolitana_di_Milano",
        "Napoli": "Comuni_della_città_metropolitana_di_Napoli",
        "Palermo": "Comuni_della_città_metropolitana_di_Palermo",
        "Reggio Calabria": "Comuni_della_città_metropolitana_di_Reggio_Calabria",
        "Roma": "Comuni_della_città_metropolitana_di_Roma_Capitale",
        "Torino": "Comuni_della_città_metropolitana_di_Torino",
        "Venezia": "Comuni_della_città_metropolitana_di_Venezia",

        # dell' articles (vowel starting regions)
        "L'Aquila": "dell'Aquila",

        # della for feminine names
        "La Spezia": "della_Spezia",

        # Autonomous provinces
        "Bolzano": "Comuni_della_provincia_autonoma_di_Bolzano",
        "Trento": "Comuni_della_provincia_autonoma_di_Trento",

        # Suppressed provinces (merged)
        "Carbonia-Iglesias": "Comuni_della_provincia_del_Sud_Sardegna",
        "Medio Campidano": "Comuni_della_provincia_del_Sud_Sardegna",
        "Ogliastra": "Comuni_della_provincia_di_Nuoro",
        "Olbia-Tempio": "Comuni_della_provincia_di_Sassari",

        # Special name formats
        "Ascoli Piceno": "Ascoli_Piceno",
        "Forlì-Cesena": "Forlì-Cesena",
        "Monza e Brianza": "Monza_e_della_Brianza",
        "Pesaro e Urbino": "Pesaro_e_Urbino",
        "Reggio Emilia": "Reggio_nell'Emilia",
        "Verbano-Cusio-Ossola": "Verbano-Cusio-Ossola",
        "Massa-Carrara": "Massa-Carrara",
        "Barletta-Andria-Trani": "Barletta-Andria-Trani",
        "Vibo Valentia": "Vibo_Valentia",
    },
}
