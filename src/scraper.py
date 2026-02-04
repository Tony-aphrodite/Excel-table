"""
Wikipedia Scraper for Municipality Data
Extracts municipality information from Wikipedia for multiple countries
Uses parallel requests for faster processing
"""
import requests
from bs4 import BeautifulSoup
import time
import re
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import urllib3
import certifi

# Use certifi SSL certificates for .exe compatibility
SSL_CERT_FILE = certifi.where()
os.environ['SSL_CERT_FILE'] = SSL_CERT_FILE
os.environ['REQUESTS_CA_BUNDLE'] = SSL_CERT_FILE

# Handle path for both script and PyInstaller .exe
if getattr(sys, 'frozen', False):
    # Running as PyInstaller .exe
    sys.path.insert(0, sys._MEIPASS)
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import REQUEST_DELAY, USER_AGENT

# Number of parallel workers (don't set too high to avoid rate limiting)
MAX_WORKERS = 5


class WikipediaScraper:
    """Scraper for municipality data from Wikipedia"""

    def __init__(self, country_config=None):
        """
        Initialize scraper with optional country configuration

        Args:
            country_config: Dictionary with country-specific settings
        """
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.municipalities = []
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        self.last_error = None  # Store last error for debugging

        # Set country configuration
        if country_config:
            self.country_config = country_config
        else:
            # Default to Spain
            from countries.spain import SPAIN_CONFIG
            self.country_config = SPAIN_CONFIG

        self.api_url = self.country_config.get("wikipedia_api")
        self.regions = self.country_config.get("regions", [])

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
        # Remove thousands separator (many countries use . for thousands)
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

    def get_region_page_title(self, region):
        """Get the Wikipedia page title for municipalities of a region"""
        mappings = self.country_config.get("region_page_mappings", {})
        pattern = self.country_config.get("page_title_pattern", "")
        default_pattern = self.country_config.get("default_region_pattern", "{region}")

        # Check if there's a direct mapping for this region
        if region in mappings:
            mapped_value = mappings[region]
            # Check if it's a full page title or just a region replacement
            full_page_prefixes = ("Lista_", "Liste_", "Anexo:", "Comuni_")
            if mapped_value.startswith(full_page_prefixes):
                return mapped_value
            region_suffix = mapped_value
        else:
            region_suffix = default_pattern.format(region=region.replace(' ', '_'))

        page_title = pattern.format(region=region_suffix)
        return page_title

    def fetch_page_html(self, page_title):
        """Fetch HTML content of a Wikipedia page with retry logic"""
        params = {
            "action": "parse",
            "page": page_title,
            "format": "json",
            "prop": "text"
        }

        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    self.api_url,
                    params=params,
                    timeout=60,
                    verify=SSL_CERT_FILE  # Use certifi SSL certificates
                )
                response.raise_for_status()
                data = response.json()

                if "parse" in data and "text" in data["parse"]:
                    return data["parse"]["text"]["*"]
                return None
            except requests.exceptions.Timeout:
                print(f"    Timeout (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
            except requests.exceptions.ConnectionError:
                print(f"    Connection error (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
            except Exception as e:
                print(f"    Error: {e} (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))

        return None

    def parse_municipalities_table(self, html_content, region):
        """Parse municipality data from HTML table"""
        if not html_content:
            return []

        # Use html.parser (built-in) instead of lxml for better .exe compatibility
        try:
            soup = BeautifulSoup(html_content, 'lxml')
        except:
            soup = BeautifulSoup(html_content, 'html.parser')
        municipalities = []

        # Find all tables - municipality data is usually in wikitables
        tables = soup.find_all('table', class_='wikitable')

        for table in tables:
            rows = table.find_all('tr')

            # Skip header row
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])

                if len(cells) >= 2:
                    municipality = self._extract_municipality_data(cells, region)
                    if municipality and municipality.get('name'):
                        municipalities.append(municipality)

        return municipalities

    def _extract_municipality_data(self, cells, region):
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
                'province': region,
                'population': population,
                'area': area,
                'density': density
            }

        except Exception as e:
            return None

    def _fetch_region_data(self, region):
        """Fetch and parse data for a single region (used by thread pool)"""
        # Create a new session for each thread to avoid thread-safety issues
        thread_session = requests.Session()
        thread_session.headers.update({"User-Agent": USER_AGENT})

        page_title = self.get_region_page_title(region)

        params = {
            "action": "parse",
            "page": page_title,
            "format": "json",
            "prop": "text"
        }

        html_content = None
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = thread_session.get(
                    self.api_url,
                    params=params,
                    timeout=60,
                    verify=SSL_CERT_FILE  # Use certifi SSL certificates
                )
                response.raise_for_status()
                data = response.json()

                if "parse" in data and "text" in data["parse"]:
                    html_content = data["parse"]["text"]["*"]
                    break
                else:
                    last_error = f"No parse data in response for {region}"
            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))

        thread_session.close()

        if last_error:
            self.last_error = last_error

        if html_content:
            municipalities = self.parse_municipalities_table(html_content, region)
            return {'region': region, 'municipalities': municipalities, 'success': True}
        else:
            return {'region': region, 'municipalities': [], 'success': False}

    def scrape_all_municipalities(self, progress_callback=None):
        """Scrape municipalities for all regions in the country using parallel requests"""
        all_municipalities = []
        total_regions = len(self.regions)
        failed_regions = []
        completed_count = 0
        lock = threading.Lock()

        def update_progress(region, count):
            nonlocal completed_count
            with lock:
                completed_count += 1
                if progress_callback:
                    progress_callback(completed_count, total_regions, region)

        try:
            # Use ThreadPoolExecutor for parallel fetching
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                # Submit all tasks
                future_to_region = {
                    executor.submit(self._fetch_region_data, region): region
                    for region in self.regions
                }

                # Process completed tasks as they finish
                for future in as_completed(future_to_region):
                    try:
                        result = future.result(timeout=120)
                        region = result['region']

                        if result['success']:
                            municipalities = result['municipalities']
                            with lock:
                                all_municipalities.extend(municipalities)
                                self.municipalities = all_municipalities.copy()
                            print(f"  Found {len(municipalities)} municipalities in {region}")
                        else:
                            print(f"  Warning: Could not fetch data for {region}")
                            failed_regions.append(region)

                        update_progress(region, len(all_municipalities))
                    except Exception as e:
                        print(f"  Error processing region: {e}")
                        failed_regions.append(future_to_region.get(future, "unknown"))

        except Exception as e:
            print(f"  Parallel processing failed: {e}")
            print("  Falling back to sequential processing...")
            # Fallback to sequential processing
            all_municipalities = []
            for idx, region in enumerate(self.regions):
                if progress_callback:
                    progress_callback(idx + 1, total_regions, region)

                result = self._fetch_region_data(region)
                if result['success']:
                    all_municipalities.extend(result['municipalities'])
                    self.municipalities = all_municipalities.copy()
                    print(f"  Found {len(result['municipalities'])} municipalities in {region}")
                else:
                    failed_regions.append(region)

                time.sleep(0.5)  # Small delay for sequential

        # Report failed regions
        if failed_regions:
            print(f"\n  Failed regions: {', '.join(failed_regions)}")
            print(f"  Successfully scraped: {total_regions - len(failed_regions)}/{total_regions}")

        self.municipalities = all_municipalities
        return all_municipalities

    def get_municipalities(self):
        """Return the scraped municipalities"""
        return self.municipalities


def main():
    """Test the scraper"""
    # Test with Spain (default)
    scraper = WikipediaScraper()

    def progress(current, total, region):
        print(f"[{current}/{total}] Scraping {region}...")

    municipalities = scraper.scrape_all_municipalities(progress_callback=progress)

    print(f"\nTotal municipalities found: {len(municipalities)}")

    # Show sample
    if municipalities:
        print("\nSample data (first 5):")
        for m in municipalities[:5]:
            print(f"  {m['name']} ({m['province']}): Pop={m['population']}, Area={m['area']}")


if __name__ == "__main__":
    main()
