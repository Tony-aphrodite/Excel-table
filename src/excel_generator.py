"""
Excel Generator for Municipality Data
Creates Excel files with municipality data and equipment calculations
Supports multiple countries with localized labels
"""
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    OUTPUT_FULL_EXCEL,
    OUTPUT_SIMPLE_EXCEL,
    COLUMN_NAMES,
    SIMPLE_COLUMNS,
    DATA_DIR,
    POPULATION_THRESHOLD,
    EQUIPMENT_DIVISOR_URBAN,
    EQUIPMENT_DIVISOR_RURAL,
    DEFAULT_URBAN_PERCENTAGE
)


class ExcelGenerator:
    """Generator for Excel files with municipality data"""

    def __init__(self, country_config=None):
        """
        Initialize generator with optional country configuration

        Args:
            country_config: Dictionary with country-specific settings
        """
        self.header_font = Font(bold=True, color="FFFFFF")
        self.header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        self.header_alignment = Alignment(horizontal="center", vertical="center")
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # Set country-specific labels or use defaults
        if country_config and "labels" in country_config:
            labels = country_config["labels"]
            self.column_names = {
                'name': labels.get('municipality', COLUMN_NAMES['name']),
                'total_hab': labels.get('total_hab', COLUMN_NAMES['total_hab']),
                'hab_urban': labels.get('hab_urban', COLUMN_NAMES['hab_urban']),
                'hab_rural': labels.get('hab_rural', COLUMN_NAMES['hab_rural']),
                'equipos_urban': labels.get('equipos_urban', COLUMN_NAMES['equipos_urban']),
                'equipos_rural': labels.get('equipos_rural', COLUMN_NAMES['equipos_rural']),
                'total_equipos': labels.get('total_equipos', COLUMN_NAMES['total_equipos']),
            }
            self.simple_columns = {
                'name': labels.get('municipality', SIMPLE_COLUMNS['name']),
                'total_equipos': labels.get('total_equipos', SIMPLE_COLUMNS['total_equipos']),
            }
            self.country_name = country_config.get("name", "España")
        else:
            self.column_names = COLUMN_NAMES
            self.simple_columns = SIMPLE_COLUMNS
            self.country_name = "España"

    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(DATA_DIR, exist_ok=True)

    def _apply_header_style(self, ws, row_num=1):
        """Apply styling to header row"""
        for cell in ws[row_num]:
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = self.header_alignment
            cell.border = self.border

    def _auto_adjust_columns(self, ws):
        """Auto-adjust column widths based on content"""
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width

    def _calculate_equipment_data(self, municipalities):
        """
        Calculate equipment data for each municipality

        Logic:
        - If population < 3000 (Rural):
            - HAB RURAL = 100% of population
            - HAB URBAN = 0
            - EQUIPOS RURAL = population / 50
            - EQUIPOS URBAN = 0

        - If population >= 3000 (Urban):
            - HAB URBAN = ~95% of population (configurable)
            - HAB RURAL = ~5% of population
            - EQUIPOS URBAN = hab_urban / 300
            - EQUIPOS RURAL = hab_rural / 50

        - TOTAL EQUIPOS = EQUIPOS URBAN + EQUIPOS RURAL
        """
        processed = []

        for m in municipalities:
            population = m.get('population') or 0
            name = m.get('name', '')

            # Determine if urban or rural based on threshold
            is_urban = population >= POPULATION_THRESHOLD

            if is_urban:
                # Urban municipality: split population into urban/rural portions
                hab_urban = int(population * DEFAULT_URBAN_PERCENTAGE)
                hab_rural = population - hab_urban

                # Calculate equipment with different divisors
                equipos_urban = round(hab_urban / EQUIPMENT_DIVISOR_URBAN, 2)
                equipos_rural = round(hab_rural / EQUIPMENT_DIVISOR_RURAL, 2)
            else:
                # Rural municipality: 100% goes to rural
                hab_urban = None  # Empty cell
                hab_rural = population

                # Calculate equipment
                equipos_urban = 0
                equipos_rural = round(population / EQUIPMENT_DIVISOR_RURAL, 2)

            # Total equipment is the sum
            total_equipos = round(equipos_urban + equipos_rural, 2)

            processed.append({
                'name': name,
                'total_hab': population,
                'hab_urban': hab_urban,
                'hab_rural': hab_rural,
                'equipos_urban': equipos_urban,
                'equipos_rural': equipos_rural,
                'total_equipos': total_equipos
            })

        return processed

    def create_full_excel(self, municipalities, output_path=None):
        """
        Create full Excel file with 7 columns

        Args:
            municipalities: List of municipality dictionaries
            output_path: Output file path (optional, uses config default)

        Returns:
            Path to created file
        """
        self._ensure_data_dir()
        output_path = output_path or OUTPUT_FULL_EXCEL

        # Calculate equipment data
        processed_data = self._calculate_equipment_data(municipalities)

        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = f"Municipios de {self.country_name}"

        # Write header
        headers = [
            self.column_names['name'],
            self.column_names['total_hab'],
            self.column_names['hab_urban'],
            self.column_names['hab_rural'],
            self.column_names['equipos_urban'],
            self.column_names['equipos_rural'],
            self.column_names['total_equipos']
        ]

        for c_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=c_idx, value=header)
            cell.border = self.border

        # Write data
        for r_idx, m in enumerate(processed_data, 2):
            ws.cell(row=r_idx, column=1, value=m['name']).border = self.border
            ws.cell(row=r_idx, column=2, value=m['total_hab']).border = self.border
            ws.cell(row=r_idx, column=3, value=m['hab_urban']).border = self.border
            ws.cell(row=r_idx, column=4, value=m['hab_rural']).border = self.border
            ws.cell(row=r_idx, column=5, value=m['equipos_urban']).border = self.border
            ws.cell(row=r_idx, column=6, value=m['equipos_rural']).border = self.border
            ws.cell(row=r_idx, column=7, value=m['total_equipos']).border = self.border

        # Apply styles
        self._apply_header_style(ws)
        self._auto_adjust_columns(ws)

        # Freeze header row
        ws.freeze_panes = 'A2'

        # Save
        wb.save(output_path)
        print(f"Full Excel saved: {output_path}")

        return output_path

    def create_simple_excel(self, municipalities, output_path=None):
        """
        Create simplified Excel file with only 2 columns

        Args:
            municipalities: List of municipality dictionaries
            output_path: Output file path (optional, uses config default)

        Returns:
            Path to created file
        """
        self._ensure_data_dir()
        output_path = output_path or OUTPUT_SIMPLE_EXCEL

        # Calculate equipment data
        processed_data = self._calculate_equipment_data(municipalities)

        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Equipos"

        # Write header
        ws.cell(row=1, column=1, value=self.simple_columns['name']).border = self.border
        ws.cell(row=1, column=2, value=self.simple_columns['total_equipos']).border = self.border

        # Write data
        for r_idx, m in enumerate(processed_data, 2):
            ws.cell(row=r_idx, column=1, value=m['name']).border = self.border
            ws.cell(row=r_idx, column=2, value=m['total_equipos']).border = self.border

        # Apply styles
        self._apply_header_style(ws)
        self._auto_adjust_columns(ws)

        # Freeze header row
        ws.freeze_panes = 'A2'

        # Save
        wb.save(output_path)
        print(f"Simple Excel saved: {output_path}")

        return output_path

    def create_both_excels(self, municipalities):
        """
        Create both full and simple Excel files

        Args:
            municipalities: List of municipality dictionaries

        Returns:
            Tuple of (full_path, simple_path)
        """
        full_path = self.create_full_excel(municipalities)
        simple_path = self.create_simple_excel(municipalities)

        return full_path, simple_path


def main():
    """Test the Excel generator"""
    generator = ExcelGenerator()

    # Test data (matching client's examples)
    test_municipalities = [
        {'name': 'Tudela', 'population': 37008},      # Urban
        {'name': 'Tafalla', 'population': 10582},     # Urban
        {'name': 'Sartaguda', 'population': 1287},    # Rural
        {'name': 'Sesma', 'population': 1149},        # Rural
        {'name': 'Sorlada', 'population': 51},        # Rural
        {'name': 'Ulzama', 'population': 1669},       # Rural
    ]

    generator.create_both_excels(test_municipalities)
    print("\nTest Excel files created successfully!")
    print(f"Urban divisor: {EQUIPMENT_DIVISOR_URBAN}")
    print(f"Rural divisor: {EQUIPMENT_DIVISOR_RURAL}")
    print(f"Default urban %: {DEFAULT_URBAN_PERCENTAGE * 100}%")


if __name__ == "__main__":
    main()
