#!/usr/bin/env python3
"""
Spanish Municipalities Excel Generator
Main entry point for the application

This script:
1. Scrapes municipality data from Spanish Wikipedia
2. Classifies each municipality as Rural or Urban (threshold: 3000 inhabitants)
3. Generates Excel files (full 6-column and simplified 2-column)
4. Generates Word document with classification data
"""
import sys
import os
from datetime import datetime
from tqdm import tqdm

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    POPULATION_THRESHOLD,
    DATA_DIR,
    OUTPUT_FULL_EXCEL,
    OUTPUT_SIMPLE_EXCEL,
    OUTPUT_WORD
)
from src.scraper import WikipediaScraper
from src.classifier import MunicipalityClassifier
from src.excel_generator import ExcelGenerator
from src.word_generator import WordGenerator


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("  Spanish Municipalities Excel Generator")
    print("  Classification: Rural (<3000) vs Urban (>=3000)")
    print("=" * 60)
    print()


def print_statistics(stats):
    """Print classification statistics"""
    print("\n" + "=" * 40)
    print("  Classification Statistics")
    print("=" * 40)
    print(f"  Total municipalities: {stats['total']}")
    print(f"  Rural (Núcleo Rural): {stats['rural']} ({stats['rural_percentage']}%)")
    print(f"  Urban (Núcleo Urbano): {stats['urban']} ({stats['urban_percentage']}%)")
    print("=" * 40)


def main():
    """Main function to orchestrate the data collection and file generation"""
    start_time = datetime.now()
    print_banner()

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Step 1: Scrape data from Wikipedia
    print("[1/4] Scraping municipality data from Wikipedia...")
    print("-" * 50)

    scraper = WikipediaScraper()

    def progress_callback(current, total, province):
        print(f"  [{current}/{total}] Fetching: {province}")

    municipalities = scraper.scrape_all_municipalities(progress_callback=progress_callback)

    if not municipalities:
        print("\nError: No municipalities were found. Please check your internet connection.")
        sys.exit(1)

    print(f"\n  Total municipalities scraped: {len(municipalities)}")

    # Step 2: Classify municipalities
    print("\n[2/4] Classifying municipalities...")
    print("-" * 50)

    classifier = MunicipalityClassifier(threshold=POPULATION_THRESHOLD)
    classified_municipalities = classifier.classify_all(municipalities)
    stats = classifier.get_statistics(classified_municipalities)

    print_statistics(stats)

    # Step 3: Generate Excel files
    print("\n[3/4] Generating Excel files...")
    print("-" * 50)

    excel_generator = ExcelGenerator()

    print("  Creating full Excel (6 columns)...")
    excel_generator.create_full_excel(classified_municipalities)

    print("  Creating simplified Excel (2 columns)...")
    excel_generator.create_simple_excel(classified_municipalities)

    # Step 4: Generate Word document
    print("\n[4/4] Generating Word document...")
    print("-" * 50)

    word_generator = WordGenerator()
    word_generator.create_word_document(classified_municipalities)

    # Summary
    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 60)
    print("  COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n  Duration: {duration}")
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
