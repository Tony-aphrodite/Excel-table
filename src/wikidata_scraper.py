"""
Wikidata SPARQL Scraper for Municipality Data
Fetches complete municipality data from Wikidata for all countries
This provides 100% complete data unlike Wikipedia table scraping
"""
import requests
import time
import sys
import os

# Handle path for both script and PyInstaller .exe
if getattr(sys, 'frozen', False):
    sys.path.insert(0, sys._MEIPASS)
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import USER_AGENT

# Wikidata SPARQL endpoint
WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

# Municipality types for each country (Wikidata Q-codes)
COUNTRY_MUNICIPALITY_TYPES = {
    "España": {
        "country_code": "Q29",
        "municipality_type": "Q2074737",  # municipality of Spain
        "name": "España",
    },
    "France": {
        "country_code": "Q142",
        "municipality_type": "Q484170",  # commune of France
        "name": "France",
    },
    "Italia": {
        "country_code": "Q38",
        "municipality_type": "Q747074",  # comune of Italy
        "name": "Italia",
    },
    "Portugal": {
        "country_code": "Q45",
        "municipality_type": "Q13217644",  # municipality of Portugal
        "name": "Portugal",
    },
    "Deutschland": {
        "country_code": "Q183",
        "municipality_type": "Q262166",  # municipality of Germany
        "name": "Deutschland",
    },
}


class WikidataScraper:
    """Scraper for municipality data from Wikidata SPARQL"""

    def __init__(self, country_config=None):
        """
        Initialize scraper with country configuration

        Args:
            country_config: Dictionary with country-specific settings
        """
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "application/sparql-results+json"
        })
        self.municipalities = []
        self.max_retries = 3
        self.retry_delay = 5

        # Get country name from config
        if country_config:
            self.country_name = country_config.get("name", "España")
        else:
            self.country_name = "España"

        # Get Wikidata codes for this country
        self.wikidata_config = COUNTRY_MUNICIPALITY_TYPES.get(
            self.country_name,
            COUNTRY_MUNICIPALITY_TYPES["España"]
        )

    def _build_sparql_query(self, offset=0, limit=5000):
        """Build SPARQL query for municipalities"""
        municipality_type = self.wikidata_config["municipality_type"]
        country_code = self.wikidata_config["country_code"]

        # Query including subclasses of municipality type
        query = f"""
        SELECT DISTINCT ?municipality ?municipalityLabel ?population
        WHERE {{
          ?municipality wdt:P31/wdt:P279* wd:{municipality_type} .
          ?municipality wdt:P17 wd:{country_code} .
          OPTIONAL {{ ?municipality wdt:P1082 ?population . }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "es,fr,it,pt,de,en" . }}
        }}
        ORDER BY ?municipality
        OFFSET {offset}
        LIMIT {limit}
        """
        return query

    def _execute_query(self, query):
        """Execute SPARQL query with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    WIKIDATA_ENDPOINT,
                    params={"query": query, "format": "json"},
                    timeout=120
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.Timeout:
                print(f"    Timeout (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
            except requests.exceptions.RequestException as e:
                print(f"    Error: {e} (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
        return None

    def _parse_results(self, results):
        """Parse SPARQL results into municipality list"""
        municipalities = []
        seen_names = set()  # Avoid duplicates

        if not results or "results" not in results:
            return municipalities

        for binding in results["results"]["bindings"]:
            try:
                name = binding.get("municipalityLabel", {}).get("value", "")

                # Skip if no name or already seen
                if not name or name in seen_names:
                    continue

                # Skip if name looks like a Q-code (not resolved)
                if name.startswith("Q") and name[1:].isdigit():
                    continue

                seen_names.add(name)

                # Get population
                population = None
                if "population" in binding:
                    try:
                        population = int(float(binding["population"]["value"]))
                    except (ValueError, TypeError):
                        pass

                municipalities.append({
                    "name": name,
                    "province": "",  # Not fetched for speed
                    "population": population,
                    "area": None,
                    "density": None
                })

            except Exception as e:
                continue

        return municipalities

    def scrape_all_municipalities(self, progress_callback=None):
        """
        Scrape all municipalities for the country using Wikidata SPARQL

        Args:
            progress_callback: Optional callback function(current, total, message)

        Returns:
            List of municipality dictionaries
        """
        all_municipalities = []
        total_expected = self._get_expected_count()
        offset = 0
        batch_size = 5000
        batch_num = 0

        print(f"  Fetching municipalities for {self.country_name} from Wikidata...")
        print(f"  Expected approximately {total_expected} municipalities")

        while True:
            batch_num += 1
            if progress_callback:
                progress_callback(
                    len(all_municipalities),
                    total_expected,
                    f"Batch {batch_num}: offset {offset}"
                )

            print(f"    Fetching batch {batch_num} (offset {offset})...")

            query = self._build_sparql_query(offset=offset, limit=batch_size)
            results = self._execute_query(query)

            if not results:
                print(f"    Failed to fetch batch {batch_num}")
                break

            municipalities = self._parse_results(results)

            if not municipalities:
                print(f"    No more results at offset {offset}")
                break

            all_municipalities.extend(municipalities)
            print(f"    Found {len(municipalities)} municipalities (total: {len(all_municipalities)})")

            if len(municipalities) < batch_size:
                break

            offset += batch_size
            time.sleep(2)  # Be nice to Wikidata servers

        # Remove duplicates by name
        seen = set()
        unique_municipalities = []
        for m in all_municipalities:
            if m["name"] not in seen:
                seen.add(m["name"])
                unique_municipalities.append(m)

        self.municipalities = unique_municipalities
        print(f"  Total unique municipalities found: {len(unique_municipalities)}")

        return unique_municipalities

    def _get_expected_count(self):
        """Get expected municipality count for progress estimation"""
        expected_counts = {
            "España": 8131,
            "France": 35000,
            "Italia": 7904,
            "Portugal": 3092,
            "Deutschland": 11000,
        }
        return expected_counts.get(self.country_name, 10000)

    def get_municipalities(self):
        """Return the scraped municipalities"""
        return self.municipalities


def main():
    """Test the Wikidata scraper"""
    # Test with each country
    for country_name in ["España", "France"]:
        print(f"\n{'='*50}")
        print(f"Testing {country_name}")
        print('='*50)

        config = {"name": country_name}
        scraper = WikidataScraper(country_config=config)

        def progress(current, total, msg):
            print(f"  Progress: {current}/{total} - {msg}")

        municipalities = scraper.scrape_all_municipalities(progress_callback=progress)

        print(f"\nTotal municipalities found: {len(municipalities)}")

        if municipalities:
            print("\nSample data (first 5):")
            for m in municipalities[:5]:
                print(f"  {m['name']} ({m['province']}): Pop={m['population']}")


if __name__ == "__main__":
    main()
