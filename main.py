#!/usr/bin/env python3
"""
Spanish Municipalities Excel Generator
Main entry point for the application

This script:
1. Scrapes municipality data from Spanish Wikipedia
2. Calculates equipment (EQUIPOS) based on population / 300
3. Generates Excel files (full 7-column and simplified 2-column)
4. Generates Word document with equipment data
"""
import sys
import os
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
from src.scraper import WikipediaScraper
from src.excel_generator import ExcelGenerator
from src.word_generator import WordGenerator


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("  Spanish Municipalities Excel Generator")
    print(f"  Urban: >= {POPULATION_THRESHOLD} hab | Rural: < {POPULATION_THRESHOLD} hab")
    print(f"  Urban Equipment = Population / {EQUIPMENT_DIVISOR_URBAN}")
    print(f"  Rural Equipment = Population / {EQUIPMENT_DIVISOR_RURAL}")
    print("=" * 60)
    print()


def print_statistics(municipalities):
    """Print statistics about the data"""
    total = len(municipalities)
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


def main():
    """Main function to orchestrate the data collection and file generation"""
    start_time = datetime.now()
    print_banner()

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Step 1: Scrape data from Wikipedia
    print("[1/3] Scraping municipality data from Wikipedia...")
    print("-" * 50)

    scraper = WikipediaScraper()

    def progress_callback(current, total, province):
        print(f"  [{current}/{total}] Fetching: {province}")

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

    excel_generator = ExcelGenerator()

    print("  Creating full Excel (7 columns)...")
    excel_generator.create_full_excel(municipalities)

    print("  Creating simplified Excel (2 columns)...")
    excel_generator.create_simple_excel(municipalities)

    # Step 3: Generate Word document
    print("\n[3/3] Generating Word document...")
    print("-" * 50)

    word_generator = WordGenerator()
    word_generator.create_word_document(municipalities)

    # Summary
    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 60)
    print("  COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n  Duration: {duration}")
    print(f"\n  Output files created:")
    print(f"    1. {OUTPUT_FULL_EXCEL}")
    print(f"       Columns: Municipio, TOTAL HAB, Nº HAB URBANO,")
    print(f"                Nº HAB RURAL, EQUIPOS URBANO,")
    print(f"                EQUIPOS RURAL, TOTAL EQUIPOS")
    print(f"    2. {OUTPUT_SIMPLE_EXCEL}")
    print(f"       Columns: Municipio, TOTAL EQUIPOS")
    print(f"    3. {OUTPUT_WORD}")
    print(f"       Columns: Municipio, TOTAL EQUIPOS")
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
