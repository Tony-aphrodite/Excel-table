@echo off
chcp 65001 > nul
echo ============================================
echo   Generador de Municipios de España
echo ============================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado.
    echo.
    echo Por favor, descargue Python desde:
    echo https://www.python.org/downloads/
    echo.
    echo Asegúrese de marcar "Add Python to PATH" durante la instalación.
    echo.
    pause
    exit /b 1
)

echo [1/3] Instalando dependencias...
pip install requests beautifulsoup4 pandas openpyxl python-docx tqdm lxml --quiet

echo [2/3] Iniciando programa...
echo.
python gui.py

pause
