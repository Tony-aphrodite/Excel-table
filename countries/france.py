"""
France country configuration
"""

FRANCE_CONFIG = {
    "name": "France",
    "language": "fr",
    "wikipedia_api": "https://fr.wikipedia.org/w/api.php",
    "wikipedia_base": "https://fr.wikipedia.org/wiki/",

    # Labels in local language
    "labels": {
        "municipality": "Commune",
        "total_hab": "TOTAL HAB",
        "hab_urban": "Nº HAB URBAIN",
        "hab_rural": "Nº HAB RURAL",
        "equipos_urban": "ÉQUIPES URBAIN",
        "equipos_rural": "ÉQUIPES RURAL",
        "total_equipos": "TOTAL ÉQUIPES",
        "rural": "Zone Rurale",
        "urban": "Zone Urbaine",
    },

    # French departments (simplified list - major departments)
    "regions": [
        "Ain", "Aisne", "Allier", "Alpes-de-Haute-Provence", "Hautes-Alpes",
        "Alpes-Maritimes", "Ardèche", "Ardennes", "Ariège", "Aube",
        "Aude", "Aveyron", "Bouches-du-Rhône", "Calvados", "Cantal",
        "Charente", "Charente-Maritime", "Cher", "Corrèze", "Corse-du-Sud",
        "Haute-Corse", "Côte-d'Or", "Côtes-d'Armor", "Creuse", "Dordogne",
        "Doubs", "Drôme", "Eure", "Eure-et-Loir", "Finistère",
        "Gard", "Haute-Garonne", "Gers", "Gironde", "Hérault",
        "Ille-et-Vilaine", "Indre", "Indre-et-Loire", "Isère", "Jura",
        "Landes", "Loir-et-Cher", "Loire", "Haute-Loire", "Loire-Atlantique",
        "Loiret", "Lot", "Lot-et-Garonne", "Lozère", "Maine-et-Loire",
        "Manche", "Marne", "Haute-Marne", "Mayenne", "Meurthe-et-Moselle",
        "Meuse", "Morbihan", "Moselle", "Nièvre", "Nord",
        "Oise", "Orne", "Pas-de-Calais", "Puy-de-Dôme", "Pyrénées-Atlantiques",
        "Hautes-Pyrénées", "Pyrénées-Orientales", "Bas-Rhin", "Haut-Rhin", "Rhône",
        "Haute-Saône", "Saône-et-Loire", "Sarthe", "Savoie", "Haute-Savoie",
        "Paris", "Seine-Maritime", "Seine-et-Marne", "Yvelines", "Deux-Sèvres",
        "Somme", "Tarn", "Tarn-et-Garonne", "Var", "Vaucluse",
        "Vendée", "Vienne", "Haute-Vienne", "Vosges", "Yonne",
        "Territoire de Belfort", "Essonne", "Hauts-de-Seine", "Seine-Saint-Denis",
        "Val-de-Marne", "Val-d'Oise"
    ],

    # Page title pattern for French Wikipedia
    "page_title_pattern": "Liste_des_communes_de_{region}",
    "default_region_pattern": "{region}",

    # Region mappings for special cases
    "region_page_mappings": {
        "Côte-d'Or": "la_Côte-d'Or",
        "Côtes-d'Armor": "des_Côtes-d'Armor",
        "Nord": "du_Nord",
        "Pas-de-Calais": "du_Pas-de-Calais",
        "Rhône": "du_Rhône",
        "Var": "du_Var",
    },
}
