"""
Excel Generator for Spanish Municipalities Data
Creates Excel files with municipality data
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
    DATA_DIR
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

    def create_full_excel(self, municipalities, output_path=None):
        """
        Create full Excel file with all 6 columns

        Args:
            municipalities: List of municipality dictionaries
            output_path: Output file path (optional, uses config default)

        Returns:
            Path to created file
        """
        self._ensure_data_dir()
        output_path = output_path or OUTPUT_FULL_EXCEL

        # Create DataFrame
        df = pd.DataFrame(municipalities)

        # Reorder and rename columns
        columns_order = ['name', 'province', 'population', 'area', 'density', 'classification']
        df = df.reindex(columns=columns_order)

        df.columns = [
            COLUMN_NAMES['name'],
            COLUMN_NAMES['province'],
            COLUMN_NAMES['population'],
            COLUMN_NAMES['area'],
            COLUMN_NAMES['density'],
            COLUMN_NAMES['classification']
        ]

        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Municipios de España"

        # Write data
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
            for c_idx, value in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                cell.border = self.border
                if r_idx > 1:
                    cell.alignment = Alignment(horizontal="left")

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
        Create simplified Excel file with only 2 columns (Name and Classification)

        Args:
            municipalities: List of municipality dictionaries
            output_path: Output file path (optional, uses config default)

        Returns:
            Path to created file
        """
        self._ensure_data_dir()
        output_path = output_path or OUTPUT_SIMPLE_EXCEL

        # Create DataFrame with only 2 columns
        df = pd.DataFrame({
            COLUMN_NAMES['name']: [m.get('name', '') for m in municipalities],
            COLUMN_NAMES['classification']: [m.get('classification', '') for m in municipalities]
        })

        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Clasificación"

        # Write data
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
            for c_idx, value in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                cell.border = self.border
                if r_idx > 1:
                    cell.alignment = Alignment(horizontal="left")

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
        {'name': 'Madrid', 'province': 'Madrid', 'population': 3223334, 'area': 604.3, 'density': 5334.23, 'classification': 'Núcleo Urbano'},
        {'name': 'Barcelona', 'province': 'Barcelona', 'population': 1620343, 'area': 101.4, 'density': 15982.18, 'classification': 'Núcleo Urbano'},
        {'name': 'Villanueva', 'province': 'Toledo', 'population': 2500, 'area': 45.2, 'density': 55.31, 'classification': 'Núcleo Rural'},
        {'name': 'Pueblecito', 'province': 'Soria', 'population': 150, 'area': 12.5, 'density': 12.0, 'classification': 'Núcleo Rural'},
    ]

    generator.create_both_excels(test_municipalities)
    print("Test Excel files created successfully!")


if __name__ == "__main__":
    main()
