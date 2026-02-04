#!/usr/bin/env python3
"""
Multi-Country Municipalities Excel Generator - GUI Version
Simple graphical interface for non-technical users
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import os

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
from src.wikidata_scraper import WikidataScraper
from src.excel_generator import ExcelGenerator
from src.word_generator import WordGenerator


class MunicipalityGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Municipios - Multi-País")
        self.root.geometry("550x520")
        self.root.resizable(False, False)

        # Center the window
        self.center_window()

        # Variables
        self.is_running = False
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Listo para comenzar")
        self.collected_municipalities = []
        self.selected_country = tk.StringVar()

        # Set default country
        available_countries = get_available_countries()
        if available_countries:
            self.selected_country.set(available_countries[0])

        # Create UI
        self.create_widgets()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Generador de Municipios",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(0, 5))

        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Genera archivos Excel y Word con datos de municipios",
            font=('Helvetica', 10)
        )
        subtitle_label.pack(pady=(0, 15))

        # Country selection frame
        country_frame = ttk.LabelFrame(main_frame, text="Selección de País", padding="10")
        country_frame.pack(fill=tk.X, pady=(0, 15))

        # Country dropdown
        country_label = ttk.Label(country_frame, text="País:")
        country_label.pack(side=tk.LEFT, padx=(0, 10))

        available_countries = get_available_countries()
        self.country_combo = ttk.Combobox(
            country_frame,
            textvariable=self.selected_country,
            values=available_countries,
            state="readonly",
            width=25
        )
        self.country_combo.pack(side=tk.LEFT)
        self.country_combo.bind('<<ComboboxSelected>>', self.on_country_change)

        # Country info label
        self.country_info_label = ttk.Label(
            country_frame,
            text="",
            font=('Helvetica', 9),
            foreground="gray"
        )
        self.country_info_label.pack(side=tk.LEFT, padx=(15, 0))
        self.update_country_info()

        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(info_frame, text=f"• Umbral Urban/Rural: {POPULATION_THRESHOLD} habitantes").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"• Equipos Urbano: Población / {EQUIPMENT_DIVISOR_URBAN}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"• Equipos Rural: Población / {EQUIPMENT_DIVISOR_RURAL}").pack(anchor=tk.W)

        # Run button
        self.run_button = ttk.Button(
            main_frame,
            text="▶  GENERAR ARCHIVOS",
            command=self.start_generation,
            style='Accent.TButton'
        )
        self.run_button.pack(pady=15, ipadx=20, ipady=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=450
        )
        self.progress_bar.pack(pady=(0, 10))

        # Status label
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=('Helvetica', 10),
            wraplength=450
        )
        self.status_label.pack(pady=(0, 15))

        # Output info
        output_frame = ttk.LabelFrame(main_frame, text="Archivos de salida", padding="10")
        output_frame.pack(fill=tk.X)

        ttk.Label(output_frame, text="📊 municipios_espana_completo.xlsx (7 columnas)").pack(anchor=tk.W)
        ttk.Label(output_frame, text="📊 municipios_espana_clasificacion.xlsx (2 columnas)").pack(anchor=tk.W)
        ttk.Label(output_frame, text="📝 municipios_espana_clasificacion.docx (2 columnas)").pack(anchor=tk.W)

        # Open folder button (initially disabled)
        self.open_folder_button = ttk.Button(
            main_frame,
            text="📁 Abrir carpeta de salida",
            command=self.open_output_folder,
            state=tk.DISABLED
        )
        self.open_folder_button.pack(pady=10)

    def on_country_change(self, event=None):
        """Handle country selection change"""
        self.update_country_info()

    def update_country_info(self):
        """Update the country info label"""
        country_name = self.selected_country.get()
        config = get_country_config(country_name)
        if config:
            num_regions = len(config.get("regions", []))
            lang = config.get("language", "?")
            self.country_info_label.config(text=f"({num_regions} regiones, Wikipedia {lang})")

    def start_generation(self):
        """Start the generation process in a separate thread"""
        if self.is_running:
            return

        self.is_running = True
        self.run_button.config(state=tk.DISABLED)
        self.country_combo.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("Iniciando...")
        self.collected_municipalities = []

        # Run in separate thread to keep GUI responsive
        thread = threading.Thread(target=self.run_generation)
        thread.daemon = True
        thread.start()

    def run_generation(self):
        """Run the actual generation process"""
        try:
            # Ensure data directory exists
            os.makedirs(DATA_DIR, exist_ok=True)

            # Get selected country config
            country_name = self.selected_country.get()
            country_config = get_country_config(country_name)

            if not country_config:
                self.show_error(f"No se encontró configuración para {country_name}")
                return

            # Step 1: Scrape data (0-70%)
            self.update_status(f"Probando conexión a Wikipedia...")

            # Test connection first
            try:
                import requests
                import certifi
                from config import USER_AGENT

                # Use certifi SSL certificates
                ssl_cert = certifi.where()

                test_response = requests.get(
                    country_config.get("wikipedia_api"),
                    params={"action": "query", "format": "json"},
                    headers={"User-Agent": USER_AGENT},
                    timeout=30,
                    verify=ssl_cert  # Use certifi SSL certificates
                )
                test_response.raise_for_status()
            except Exception as e:
                self.show_error(
                    f"No se puede conectar a Wikipedia.\n\n"
                    f"Error: {str(e)}\n\n"
                    f"URL: {country_config.get('wikipedia_api')}\n\n"
                    f"Verifique su conexión a internet y firewall."
                )
                return

            # Try both Wikidata and Wikipedia, use the one with more results
            municipalities = []

            # Thread-safe progress update function
            def do_progress_update(p, msg):
                self.progress_var.set(p)
                self.status_var.set(msg)
                self.root.update_idletasks()

            # Try Wikidata first
            wikidata_municipalities = []
            try:
                self.update_status(f"Probando Wikidata ({country_name})...")
                wikidata_scraper = WikidataScraper(country_config=country_config)

                def wikidata_progress(current, total, msg):
                    progress = min((current / max(total, 1)) * 35, 35)
                    self.root.after(0, lambda: do_progress_update(progress, f"Wikidata: {current} municipios..."))

                wikidata_municipalities = wikidata_scraper.scrape_all_municipalities(progress_callback=wikidata_progress)
                self.update_status(f"Wikidata: {len(wikidata_municipalities)} municipios")
            except Exception as e:
                print(f"Wikidata error: {e}")

            # Also try Wikipedia
            wiki_municipalities = []
            try:
                self.update_status(f"Descargando de Wikipedia ({country_name})...")
                scraper = WikipediaScraper(country_config=country_config)
                total_regions = len(country_config.get("regions", []))

                def wiki_progress_callback(current, total, region):
                    progress = 35 + (current / total) * 35
                    count = len(scraper.municipalities) if hasattr(scraper, 'municipalities') else 0
                    self.root.after(0, lambda: do_progress_update(progress, f"Wikipedia [{current}/{total}] {region}... ({count})"))

                wiki_municipalities = scraper.scrape_all_municipalities(progress_callback=wiki_progress_callback)
                self.update_status(f"Wikipedia: {len(wiki_municipalities)} municipios")
            except Exception as e:
                print(f"Wikipedia error: {e}")

            # Use the source with more results
            if len(wikidata_municipalities) >= len(wiki_municipalities):
                municipalities = wikidata_municipalities
                source = "Wikidata"
            else:
                municipalities = wiki_municipalities
                source = "Wikipedia"

            self.update_status(f"Usando {source}: {len(municipalities)} municipios")
            self.collected_municipalities = municipalities

            # Check if we got any data
            if not municipalities:
                error_detail = ""
                if hasattr(scraper, 'last_error') and scraper.last_error:
                    error_detail = f"\n\nDetalle: {scraper.last_error}"

                self.show_error(
                    "No se encontraron municipios.\n\n"
                    "Posibles causas:\n"
                    "• Sin conexión a internet\n"
                    "• Wikipedia no está disponible\n"
                    "• Firewall bloqueando conexiones\n\n"
                    f"Verifique su conexión e intente de nuevo.{error_detail}"
                )
                return

            # Even if we got partial data, continue
            if len(municipalities) < total_regions * 50:  # Rough estimate
                self.update_status(f"⚠ Datos parciales: {len(municipalities)} municipios")

            # Step 2: Generate Excel files (70-90%)
            self.progress_var.set(75)
            self.update_status(f"Generando Excel ({len(municipalities)} municipios)...")

            excel_generator = ExcelGenerator(country_config=country_config)
            excel_generator.create_full_excel(municipalities)

            self.progress_var.set(85)
            excel_generator.create_simple_excel(municipalities)

            # Step 3: Generate Word document (90-100%)
            self.progress_var.set(92)
            self.update_status("Generando documento Word...")

            word_generator = WordGenerator(country_config=country_config)
            word_generator.create_word_document(municipalities)

            # Complete
            self.progress_var.set(100)
            self.update_status(f"✓ Completado: {len(municipalities)} municipios de {country_name}")
            self.open_folder_button.config(state=tk.NORMAL)

            # Show success message
            self.root.after(100, lambda: messagebox.showinfo(
                "Completado",
                f"Archivos generados exitosamente!\n\n"
                f"• País: {country_name}\n"
                f"• {len(municipalities)} municipios procesados\n"
                f"• Archivos guardados en: data/\n\n"
                f"Haga clic en 'Abrir carpeta de salida' para ver los archivos."
            ))

        except Exception as e:
            error_msg = str(e)
            # If we collected some data, try to save it anyway
            if self.collected_municipalities and len(self.collected_municipalities) > 0:
                try:
                    country_name = self.selected_country.get()
                    country_config = get_country_config(country_name)

                    self.update_status(f"Error parcial. Guardando {len(self.collected_municipalities)} municipios...")
                    excel_generator = ExcelGenerator(country_config=country_config)
                    excel_generator.create_full_excel(self.collected_municipalities)
                    excel_generator.create_simple_excel(self.collected_municipalities)
                    word_generator = WordGenerator(country_config=country_config)
                    word_generator.create_word_document(self.collected_municipalities)
                    self.open_folder_button.config(state=tk.NORMAL)
                    self.show_error(
                        f"Error durante la descarga, pero se guardaron {len(self.collected_municipalities)} municipios.\n\n"
                        f"Error: {error_msg}\n\n"
                        f"Los archivos parciales están en la carpeta 'data/'."
                    )
                except:
                    self.show_error(f"Error: {error_msg}")
            else:
                self.show_error(f"Error: {error_msg}")
        finally:
            self.is_running = False
            self.run_button.config(state=tk.NORMAL)
            self.country_combo.config(state="readonly")

    def update_status(self, message):
        """Update status label (thread-safe)"""
        self.root.after(0, lambda: self.status_var.set(message))

    def show_error(self, message):
        """Show error message (thread-safe)"""
        self.root.after(0, lambda: messagebox.showerror("Error", message))
        self.root.after(0, lambda: self.status_var.set("Error - Ver mensaje"))
        self.root.after(0, lambda: self.progress_var.set(0))

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        import subprocess
        import platform

        try:
            if platform.system() == "Windows":
                os.startfile(DATA_DIR)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", DATA_DIR])
            else:  # Linux
                subprocess.Popen(["xdg-open", DATA_DIR])
        except Exception as e:
            messagebox.showinfo("Carpeta", f"Los archivos están en:\n{DATA_DIR}")


def main():
    root = tk.Tk()

    # Try to set a modern theme
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "light")
    except:
        pass  # Use default theme if azure not available

    app = MunicipalityGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
