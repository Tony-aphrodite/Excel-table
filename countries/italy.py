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

    # Region mappings for special cases
    "region_page_mappings": {
        "L'Aquila": "dell'Aquila",
        "La Spezia": "della_Spezia",
    },
}
