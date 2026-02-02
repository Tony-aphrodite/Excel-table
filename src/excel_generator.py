"""
Excel Generator for Spanish Municipalities Data
Creates Excel files with municipality data and equipment calculations
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
    EQUIPMENT_DIVISOR
)


class ExcelGenerator:
    """Generator for Excel files with municipality data"""

    def __init__(self):
        self.header_font = Font(bold=True, color="FFFFFF")
        self.header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        self.header_alignment = Alignment(horizontal="center", vertical="center")
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

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
        - If population >= 3000: Urban (HAB URBANO = population, EQUIPOS URBANO = population/300)
        - If population < 3000: Rural (HAB RURAL = population, EQUIPOS RURAL = population/300)
        """
        processed = []

        for m in municipalities:
            population = m.get('population') or 0
            name = m.get('name', '')

            # Determine if urban or rural
            is_urban = population >= POPULATION_THRESHOLD

            # Calculate values
            hab_urban = population if is_urban else None
            hab_rural = population if not is_urban else None
            equipos_urban = round(population / EQUIPMENT_DIVISOR, 2) if is_urban else 0
            equipos_rural = round(population / EQUIPMENT_DIVISOR, 2) if not is_urban else 0
            total_equipos = round(population / EQUIPMENT_DIVISOR, 2)

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
        Create full Excel file with 7 columns:
        Municipio, TOTAL HAB, Nº HAB URBANO, Nº HAB RURAL,
        EQUIPOS URBANO, EQUIPOS RURAL, TOTAL EQUIPOS

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
        ws.title = "Municipios de España"

        # Write header
        headers = [
            COLUMN_NAMES['name'],
            COLUMN_NAMES['total_hab'],
            COLUMN_NAMES['hab_urban'],
            COLUMN_NAMES['hab_rural'],
            COLUMN_NAMES['equipos_urban'],
            COLUMN_NAMES['equipos_rural'],
            COLUMN_NAMES['total_equipos']
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
        Create simplified Excel file with only 2 columns:
        Municipio, TOTAL EQUIPOS

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
        ws.cell(row=1, column=1, value=SIMPLE_COLUMNS['name']).border = self.border
        ws.cell(row=1, column=2, value=SIMPLE_COLUMNS['total_equipos']).border = self.border

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

    # Test data
    test_municipalities = [
        {'name': 'Madrid', 'population': 3223334},
        {'name': 'Barcelona', 'population': 1620343},
        {'name': 'Tudela', 'population': 37008},
        {'name': 'Tafalla', 'population': 10582},
        {'name': 'Villanueva', 'population': 2500},
        {'name': 'Pueblecito', 'population': 150},
        {'name': 'Sartaguda', 'population': 1287},
    ]

    generator.create_both_excels(test_municipalities)
    print("Test Excel files created successfully!")


if __name__ == "__main__":
    main()
