#!/usr/bin/env python3
"""
Multi-Country Municipalities Excel Generator
Main entry point for the CLI application

This script:
1. Scrapes municipality data from Wikipedia for the selected country
2. Calculates equipment (EQUIPOS) based on population
3. Generates Excel files (full 7-column and simplified 2-column)
4. Generates Word document with equipment data
"""
import sys
import os
import argparse
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    POPULATION_THRESHOLD,
    EQUIPMENT_DIVISOR_URBAN,
    EQUIPMENT_DIVISOR_RURAL,
    DATA_DIR,
    OUTPUT_FULL_EXCEL,
    OUTPUT_SIMPLE_EXCEL,
    OUTPUT_WORD
)
from countries import get_country_config, get_available_countries
from src.scraper import WikipediaScraper
from src.excel_generator import ExcelGenerator
from src.word_generator import WordGenerator


def print_banner(country_name):
    """Print application banner"""
    print("=" * 60)
    print("  Multi-Country Municipalities Excel Generator")
    print(f"  Country: {country_name}")
    print(f"  Urban: >= {POPULATION_THRESHOLD} hab | Rural: < {POPULATION_THRESHOLD} hab")
    print(f"  Urban Equipment = Population / {EQUIPMENT_DIVISOR_URBAN}")
    print(f"  Rural Equipment = Population / {EQUIPMENT_DIVISOR_RURAL}")
    print("=" * 60)
    print()


def print_statistics(municipalities):
    """Print statistics about the data"""
    total = len(municipalities)
    if total == 0:
        print("  No municipalities found.")
        return

    urban_count = sum(1 for m in municipalities if (m.get('population') or 0) >= POPULATION_THRESHOLD)
    rural_count = total - urban_count

    total_pop = sum(m.get('population') or 0 for m in municipalities)
    urban_pop = sum(m.get('population') or 0 for m in municipalities if (m.get('population') or 0) >= POPULATION_THRESHOLD)
    rural_pop = total_pop - urban_pop

    print("\n" + "=" * 50)
    print("  Statistics")
    print("=" * 50)
    print(f"  Total municipalities: {total}")
    print(f"  Urban (>= {POPULATION_THRESHOLD}): {urban_count} ({round(urban_count/total*100, 1)}%)")
    print(f"  Rural (< {POPULATION_THRESHOLD}): {rural_count} ({round(rural_count/total*100, 1)}%)")
    print(f"  Total population: {total_pop:,}")
    print("=" * 50)


def list_countries():
    """List all available countries"""
    print("\nAvailable countries:")
    print("-" * 40)
    for country in get_available_countries():
        config = get_country_config(country)
        regions = len(config.get("regions", []))
        lang = config.get("language", "?")
        print(f"  • {country} ({regions} regions, Wikipedia {lang})")
    print()


def main():
    """Main function to orchestrate the data collection and file generation"""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Multi-Country Municipalities Excel Generator")
    parser.add_argument(
        "-c", "--country",
        default="España",
        help="Country to process (default: España)"
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List available countries"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch GUI mode"
    )
    args = parser.parse_args()

    # List countries mode
    if args.list:
        list_countries()
        return

    # GUI mode
    if args.gui:
        from gui import main as gui_main
        gui_main()
        return

    # Get country configuration
    country_config = get_country_config(args.country)
    if not country_config:
        print(f"Error: Unknown country '{args.country}'")
        list_countries()
        sys.exit(1)

    start_time = datetime.now()
    print_banner(args.country)

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Step 1: Scrape data from Wikipedia
    print("[1/3] Scraping municipality data from Wikipedia...")
    print("-" * 50)

    scraper = WikipediaScraper(country_config=country_config)

    def progress_callback(current, total, region):
        print(f"  [{current}/{total}] Fetching: {region}")

    municipalities = scraper.scrape_all_municipalities(progress_callback=progress_callback)

    if not municipalities:
        print("\nError: No municipalities were found. Please check your internet connection.")
        sys.exit(1)

    print(f"\n  Total municipalities scraped: {len(municipalities)}")

    # Print statistics
    print_statistics(municipalities)

    # Step 2: Generate Excel files
    print("\n[2/3] Generating Excel files...")
    print("-" * 50)

    excel_generator = ExcelGenerator(country_config=country_config)

    print("  Creating full Excel (7 columns)...")
    excel_generator.create_full_excel(municipalities)

    print("  Creating simplified Excel (2 columns)...")
    excel_generator.create_simple_excel(municipalities)

    # Step 3: Generate Word document
    print("\n[3/3] Generating Word document...")
    print("-" * 50)

    word_generator = WordGenerator(country_config=country_config)
    word_generator.create_word_document(municipalities)

    # Summary
    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 60)
    print("  COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n  Country: {args.country}")
    print(f"  Duration: {duration}")
    print(f"\n  Output files created:")
    print(f"    1. {OUTPUT_FULL_EXCEL}")
    print(f"    2. {OUTPUT_SIMPLE_EXCEL}")
    print(f"    3. {OUTPUT_WORD}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
