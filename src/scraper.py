"""
Wikipedia Scraper for Spanish Municipalities Data
Extracts municipality information from Spanish Wikipedia
"""
import requests
from bs4 import BeautifulSoup
import time
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    WIKIPEDIA_API_URL,
    REQUEST_DELAY,
    USER_AGENT,
    SPANISH_PROVINCES
)


class WikipediaScraper:
    """Scraper for Spanish municipality data from Wikipedia"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.municipalities = []

    def _clean_number(self, text):
        """Clean and parse numeric values from text"""
        if not text:
            return None
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', str(text))
        # Remove references like [1], [2], etc.
        text = re.sub(r'\[[^\]]*\]', '', text)
        # Remove spaces and non-breaking spaces
        text = text.replace('\xa0', '').replace(' ', '').replace(',', '.').strip()
        # Remove thousands separator (Spanish uses . for thousands)
        text = re.sub(r'\.(?=\d{3})', '', text)
        # Try to extract number
        match = re.search(r'[\d]+[.,]?\d*', text)
        if match:
            try:
                return float(match.group().replace(',', '.'))
            except ValueError:
                return None
        return None

    def _clean_text(self, text):
        """Clean text by removing references and extra whitespace"""
        if not text:
            return ""
        text = re.sub(r'\[[^\]]*\]', '', str(text))
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

    def get_province_municipalities_page(self, province):
        """Get the Wikipedia page for municipalities of a province"""
        # Different provinces have different page naming conventions
        province_mappings = {
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
        }

        suffix = province_mappings.get(province, f"la_provincia_de_{province.replace(' ', '_')}")
        page_title = f"Anexo:Municipios_de_{suffix}"

        return page_title

    def fetch_page_html(self, page_title):
        """Fetch HTML content of a Wikipedia page"""
        params = {
            "action": "parse",
            "page": page_title,
            "format": "json",
            "prop": "text"
        }

        try:
            response = self.session.get(WIKIPEDIA_API_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if "parse" in data and "text" in data["parse"]:
                return data["parse"]["text"]["*"]
            return None
        except Exception as e:
            print(f"Error fetching {page_title}: {e}")
            return None

    def parse_municipalities_table(self, html_content, province):
        """Parse municipality data from HTML table"""
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'lxml')
        municipalities = []

        # Find all tables - municipality data is usually in wikitables
        tables = soup.find_all('table', class_='wikitable')

        for table in tables:
            rows = table.find_all('tr')

            # Skip header row
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])

                if len(cells) >= 2:
                    municipality = self._extract_municipality_data(cells, province)
                    if municipality and municipality.get('name'):
                        municipalities.append(municipality)

        return municipalities

    def _extract_municipality_data(self, cells, province):
        """Extract municipality data from table cells"""
        try:
            # First cell is usually the municipality name
            name_cell = cells[0]
            name = self._clean_text(name_cell.get_text())

            if not name or len(name) < 2:
                return None

            # Try to find population and area in remaining cells
            population = None
            area = None

            for i, cell in enumerate(cells[1:], 1):
                cell_text = cell.get_text()
                cell_num = self._clean_number(cell_text)

                if cell_num is not None:
                    # Heuristic: population is usually larger than area
                    # Area is usually < 2000 km², population can be any number
                    if population is None:
                        if cell_num > 10:  # Likely population
                            population = int(cell_num)
                        elif cell_num > 0:  # Could be area
                            area = cell_num
                    elif area is None:
                        if cell_num < 2000 and cell_num > 0:  # Likely area
                            area = cell_num

            # Calculate density if we have both values
            density = None
            if population is not None and area is not None and area > 0:
                density = round(population / area, 2)

            return {
                'name': name,
                'province': province,
                'population': population,
                'area': area,
                'density': density
            }

        except Exception as e:
            return None

    def scrape_all_municipalities(self, progress_callback=None):
        """Scrape municipalities for all Spanish provinces"""
        all_municipalities = []
        total_provinces = len(SPANISH_PROVINCES)

        for idx, province in enumerate(SPANISH_PROVINCES):
            if progress_callback:
                progress_callback(idx + 1, total_provinces, province)

            page_title = self.get_province_municipalities_page(province)
            html_content = self.fetch_page_html(page_title)

            if html_content:
                municipalities = self.parse_municipalities_table(html_content, province)
                all_municipalities.extend(municipalities)
                print(f"  Found {len(municipalities)} municipalities in {province}")
            else:
                print(f"  Warning: Could not fetch data for {province}")

            # Rate limiting
            time.sleep(REQUEST_DELAY)

        self.municipalities = all_municipalities
        return all_municipalities

    def get_municipalities(self):
        """Return the scraped municipalities"""
        return self.municipalities


def main():
    """Test the scraper"""
    scraper = WikipediaScraper()

    def progress(current, total, province):
        print(f"[{current}/{total}] Scraping {province}...")

    municipalities = scraper.scrape_all_municipalities(progress_callback=progress)

    print(f"\nTotal municipalities found: {len(municipalities)}")

    # Show sample
    if municipalities:
        print("\nSample data (first 5):")
        for m in municipalities[:5]:
            print(f"  {m['name']} ({m['province']}): Pop={m['population']}, Area={m['area']}")


if __name__ == "__main__":
    main()
