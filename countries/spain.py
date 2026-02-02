"""
Spain country configuration
"""

SPAIN_CONFIG = {
    "name": "España",
    "language": "es",
    "wikipedia_api": "https://es.wikipedia.org/w/api.php",
    "wikipedia_base": "https://es.wikipedia.org/wiki/",

    # Labels in local language
    "labels": {
        "municipality": "Municipio",
        "total_hab": "TOTAL HAB",
        "hab_urban": "Nº HAB URBANO",
        "hab_rural": "Nº HAB RURAL",
        "equipos_urban": "EQUIPOS URBANO",
        "equipos_rural": "EQUIPOS RURAL",
        "total_equipos": "TOTAL EQUIPOS",
        "rural": "Núcleo Rural",
        "urban": "Núcleo Urbano",
    },

    # Regions/Provinces
    "regions": [
        "A Coruña", "Álava", "Albacete", "Alicante", "Almería", "Asturias",
        "Ávila", "Badajoz", "Barcelona", "Bizkaia", "Burgos", "Cáceres",
        "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca",
        "Gipuzkoa", "Girona", "Granada", "Guadalajara", "Huelva", "Huesca",
        "Illes Balears", "Jaén", "La Rioja", "Las Palmas", "León", "Lleida",
        "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", "Palencia",
        "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia", "Sevilla",
        "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid",
        "Zamora", "Zaragoza"
    ],

    # Wikipedia page title mappings
    "region_page_mappings": {
        "A Coruña": "la_provincia_de_La_Coruña",
        "Álava": "la_provincia_de_Álava",
        "Alicante": "la_provincia_de_Alicante",
        "Almería": "la_provincia_de_Almería",
        "Asturias": "Asturias",
        "Ávila": "la_provincia_de_Ávila",
        "Badajoz": "la_provincia_de_Badajoz",
        "Barcelona": "la_provincia_de_Barcelona",
        "Bizkaia": "Vizcaya",
        "Burgos": "la_provincia_de_Burgos",
        "Cáceres": "la_provincia_de_Cáceres",
        "Cádiz": "la_provincia_de_Cádiz",
        "Cantabria": "Cantabria",
        "Castellón": "la_provincia_de_Castellón",
        "Ciudad Real": "la_provincia_de_Ciudad_Real",
        "Córdoba": "la_provincia_de_Córdoba",
        "Cuenca": "la_provincia_de_Cuenca",
        "Gipuzkoa": "Guipúzcoa",
        "Girona": "la_provincia_de_Gerona",
        "Granada": "la_provincia_de_Granada",
        "Guadalajara": "la_provincia_de_Guadalajara",
        "Huelva": "la_provincia_de_Huelva",
        "Huesca": "la_provincia_de_Huesca",
        "Illes Balears": "las_Islas_Baleares",
        "Jaén": "la_provincia_de_Jaén",
        "La Rioja": "La_Rioja",
        "Las Palmas": "la_provincia_de_Las_Palmas",
        "León": "la_provincia_de_León",
        "Lleida": "la_provincia_de_Lérida",
        "Lugo": "la_provincia_de_Lugo",
        "Madrid": "la_Comunidad_de_Madrid",
        "Málaga": "la_provincia_de_Málaga",
        "Murcia": "la_Región_de_Murcia",
        "Navarra": "Navarra",
        "Ourense": "la_provincia_de_Orense",
        "Palencia": "la_provincia_de_Palencia",
        "Pontevedra": "la_provincia_de_Pontevedra",
        "Salamanca": "la_provincia_de_Salamanca",
        "Santa Cruz de Tenerife": "la_provincia_de_Santa_Cruz_de_Tenerife",
        "Segovia": "la_provincia_de_Segovia",
        "Sevilla": "la_provincia_de_Sevilla",
        "Soria": "la_provincia_de_Soria",
        "Tarragona": "la_provincia_de_Tarragona",
        "Teruel": "la_provincia_de_Teruel",
        "Toledo": "la_provincia_de_Toledo",
        "Valencia": "la_provincia_de_Valencia",
        "Valladolid": "la_provincia_de_Valladolid",
        "Zamora": "la_provincia_de_Zamora",
        "Zaragoza": "la_provincia_de_Zaragoza",
        "Albacete": "la_provincia_de_Albacete"
    },

    # Page title pattern
    "page_title_pattern": "Anexo:Municipios_de_{region}",
    "default_region_pattern": "la_provincia_de_{region}",
}
